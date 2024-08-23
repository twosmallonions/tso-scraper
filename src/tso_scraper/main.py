from fastapi import FastAPI

from tso_scraper.scrape import route as scrape

app = FastAPI(
    swagger_ui_init_oauth={
        'clientId': 'tso-api-docs',
        'usePkceWithAuthorizationCodeGrant': True,
        'scopes': 'openid',
    }
)

app.include_router(scrape.router)
