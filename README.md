## Generate protobuf files
```sh
cd src
uv run python -m grpc_tools.protoc --proto_path=tso_scraper/generated=..\protobuf --python_out=. --grpc_python_out=. --pyi_out=. ..\protobuf\recipe.proto
```