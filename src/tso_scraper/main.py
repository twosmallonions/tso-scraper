import asyncio
import logging
import os
from pathlib import Path

import grpc
from grpc_reflection.v1alpha import reflection

from tso_scraper.generated import healthcheck_pb2, healthcheck_pb2_grpc, recipe_pb2, recipe_pb2_grpc
from tso_scraper.recipe_scraper import RecipeScrapers

_cleanup_coroutines = []


def load_credentials_from_file(path: str | Path) -> bytes:
    if isinstance(path, str):
        path = Path(path)

    if not path.absolute():
        msg = f"'{path}' path has to be absolute."
        raise ValueError(msg)

    with path.open('rb') as f:
        return f.read()


SERVER_CERTIFICATE = load_credentials_from_file(os.environ['SCRAPER_SERVER_CERT'])
SERVER_CERTIFICATE_KEY = load_credentials_from_file(os.environ['SCRAPER_SERVER_CERT_KEY'])
ROOT_CA = load_credentials_from_file(os.environ['SCRAPER_CA_CERT'])

HEALTHCHECK_WATCH_DELAY = 2


class Healthcheck(healthcheck_pb2_grpc.HealthServicer):
    def __init__(self) -> None:
        self.status = healthcheck_pb2.HealthCheckResponse.NOT_SERVING

    def set_status(self, status: healthcheck_pb2.HealthCheckResponse.ServingStatus):
        self.status = status

    async def Check(  # noqa: N802
        self,
        request: healthcheck_pb2.HealthCheckRequest,  # noqa: ARG002
        context: grpc.aio.ServicerContext,  # noqa: ARG002
    ) -> healthcheck_pb2.HealthCheckResponse:
        return healthcheck_pb2.HealthCheckResponse(status=self.status)

    async def Watch(self, request, context: grpc.aio.ServicerContext):  # noqa: ARG002, N802
        try:
            while not context.done():
                yield healthcheck_pb2.HealthCheckResponse(status=self.status)
                await asyncio.sleep(HEALTHCHECK_WATCH_DELAY)
        except asyncio.CancelledError:
            return


class Scraper(recipe_pb2_grpc.ScraperService):
    def __init__(self) -> None:
        self.recipe_scrapers = RecipeScrapers()

    async def Scrape(  # noqa: N802 # type: ignore
        self,
        request: recipe_pb2.ScrapeRequest,
        context: grpc.aio.ServicerContext,  # noqa: ARG002
    ) -> recipe_pb2.ScrapeResponse:
        recipe = await self.recipe_scrapers.scrape(request.url)
        ingredient_groups = [
            recipe_pb2.ScrapeResponse.IngredientGroup(
                ingredients=ingredient_group['ingredients'], purpose=ingredient_group['purpose']
            )
            for ingredient_group in recipe.get('ingredient_groups', [])
        ]
        return recipe_pb2.ScrapeResponse(
            author=recipe.get('author'),
            canonical_url=recipe.get('canonical_url'),
            category=recipe.get('category'),
            cook_time=recipe.get('cook_time'),
            description=recipe.get('description'),
            image=recipe.get('image'),
            ingredients=recipe.get('ingredients', []),
            instructions=recipe.get('instructions'),
            instructions_list=recipe.get('instructions_list', []),
            keywords=recipe.get('keywords', []),
            language=recipe.get('language'),
            prep_time=recipe.get('prep_time'),
            title=recipe.get('title'),
            total_time=recipe.get('total_time'),
            cuisine=recipe.get('cuisine'),
            host=recipe.get('host'),
            ingredient_groups=ingredient_groups,
        )


async def main() -> None:
    server = grpc.aio.server()
    recipe_pb2_grpc.add_ScraperServiceServicer_to_server(Scraper(), server)

    healthcheck = Healthcheck()
    healthcheck_pb2_grpc.add_HealthServicer_to_server(healthcheck, server)

    listen_addr = '[::]:50051'
    server_credentials = grpc.ssl_server_credentials(
        private_key_certificate_chain_pairs=((SERVER_CERTIFICATE_KEY, SERVER_CERTIFICATE),),
        root_certificates=ROOT_CA,
        require_client_auth=True,
    )

    service_names = (
        recipe_pb2.DESCRIPTOR.services_by_name['ScraperService'].full_name,
        healthcheck_pb2.DESCRIPTOR.services_by_name['Health'].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(service_names, server)

    server.add_secure_port('0.0.0.0:50051', server_credentials)
    server.add_insecure_port('0.0.0.0:23867')

    logging.info('Starting server on %s', listen_addr)

    await server.start()
    healthcheck.set_status(healthcheck_pb2.HealthCheckResponse.SERVING)

    async def server_graceful_shutdown():
        logging.info('Shutting down...')
        await server.stop(5)

    _cleanup_coroutines.append(server_graceful_shutdown)

    await server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    finally:
        loop.run_until_complete(*_cleanup_coroutines)
        loop.close()
