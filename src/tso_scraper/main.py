import asyncio
import logging
from operator import ge
import os
from pathlib import Path

import grpc

from tso_scraper.generated import recipe_pb2, recipe_pb2_grpc
from tso_scraper.recipe_scraper import RecipeScrapers


def load_credentials_from_file(path: str | Path) -> bytes:
    if isinstance(path, str):
        path = Path(path)

    if not path.absolute():
        msg = f"'{path}' path has to be aboslute."
        raise ValueError(msg)

    with path.open('rb') as f:
        return f.read()


SERVER_CERTIFICATE = load_credentials_from_file(os.environ['SCRAPER_SERVER_CERT'])
SERVER_CERTIFICATE_KEY = load_credentials_from_file(os.environ['SCRAPER_SERVER_CERT_KEY'])
ROOT_CA = load_credentials_from_file(os.environ['SCRAPER_CA_CERT'])


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
            recipe_pb2.ScrapeResponse.IngredientGroup(ingredients=ingredient_group['ingredients'], purpose=ingredient_group['purpose'])
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
            ingredient_groups=ingredient_groups
        )


async def main() -> None:
    server = grpc.aio.server()
    recipe_pb2_grpc.add_ScraperServiceServicer_to_server(Scraper(), server)
    listen_addr = '[::]:50051'
    server_credentials = grpc.ssl_server_credentials(
        private_key_certificate_chain_pairs=((SERVER_CERTIFICATE_KEY, SERVER_CERTIFICATE),),
        root_certificates=ROOT_CA,
        require_client_auth=True,
    )
    server.add_secure_port('0.0.0.0:50051', server_credentials)
    logging.info('Starting server on %s', listen_addr)
    await server.start()
    await server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(main())
