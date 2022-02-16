#!/bin/bash

celery -A api worker -f celery.logs --loglevel=DEBUG