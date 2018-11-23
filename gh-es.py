#!/usr/bin/env python
import argparse
import os

from github import Github
from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk

def gen_docs(gh):
    org = gh.get_organization(args.org)
    for r in org.get_repos():
        for t in r.get_tags():
            yield {
                'organization': org.name,
                'repository': r.name,
                'tag': t.name,
            }

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-O", "--org",
        action="store",
        default="elastic",
        help="Github organization to fetch repos and tags from. (Default: elastic")
    parser.add_argument(
        "-H", "--host",
        action="store",
        default="localhost:9200",
        help="ES X-Pack host to connect to. (Default: https://localhost:9200)")
    parser.add_argument(
        "-U", "--user",
        action="store",
        default="gh-inventory",
        help="ES user to connect with. (Default: gh-inventory)")

    args = parser.parse_args()
    
    auth = (args.user, os.environ['ES_XPACK_PASSWORD'])
    es = Elasticsearch(args.host, scheme='https', http_auth=auth, ca_certs=os.environ['ES_XPACK_CA_CERT_PATH']) 

    index_tmpl = {
      'settings': {
        'number_of_shards': 1,
        'number_of_replicas': 0
      },
      'mappings': {
        'doc': {
          'properties': {
            'organization': {'type': 'keyword'},
            'repository': {'type': 'keyword'},
            'tag': {'type': 'text'}
          }
        }
      }
    }

    es.indices.create(
        index='gh-inventory',
        body=index_tmpl)

    gh = Github(os.environ['GH_ACCESS_TOKEN'])

    for ok, result in streaming_bulk(
            es,
            gen_docs(gh),
            index='gh-inventory',
            doc_type='doc',
            chunk_size=50
        ):
        _, result = result.popitem()
        if not ok:
            print("indexing failed, %s" % result)
        else:
            print("indexing succeeded, %s" % result['_id'])
