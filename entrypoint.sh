#!/bin/bash

alembic upgrade head
uvicorn api.main:memourse.create_app --factory --host 0.0.0.0