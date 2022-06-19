#!/bin/bash

alias curlapi="curl -v -H 'Accept: application/json; indent=4' -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:101.0) Gecko/20100101 Firefox/101.0'";
API_BASE='https://oe.datalisk.io/matchData';

function matchdata() {
    curlapi  -H 'X-Api-Key: f561197a-82ea-4e54-acd2-386979018a7a' $API_BASE -o match_data.json
}