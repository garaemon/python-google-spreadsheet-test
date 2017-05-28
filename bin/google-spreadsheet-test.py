#!/usr/bin/env python

import os
from urllib.parse import urlparse

import fire
import inquirer
import gspread
from oauth2client.service_account import ServiceAccountCredentials


class App(object):
    def parse_document_id_from_url(self, url):
        if url.startswith('https://'):
            parsed_url = urlparse(url)
            url_path = parsed_url.path
            return url_path.split('/')[3]
        else:
            return url

    def run(self, doc_id=None, cred_json=None):
        if doc_id is None:
            doc_id = inquirer.prompt([inquirer.Text(
                'doc_id',
                message='Please enter document id or url')])['doc_id']
        if cred_json is None:
            cred_json = inquirer.prompt([inquirer.Text(
                'cred_json',
                message='Please enter credential json file')])['cred_json']
        if not os.path.exists(os.path.expanduser(cred_json)):
            raise Exception('Cannot find {}'.format(cred_json))
        doc_id = self.parse_document_id_from_url(doc_id)
        print('doc_id = {}'.format(doc_id))
        print('cred_json = {}'.format(cred_json))
        scope = ['https://spreadsheets.google.com/feeds']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            os.path.expanduser(cred_json), scope)
        client = gspread.authorize(credentials)
        gfile = client.open_by_key(doc_id)
        worksheet = gfile.sheet1
        records = worksheet.get_all_values()

        print('Success to access to {}'.format(doc_id))

        for record in records:
            print(record)


if __name__ == '__main__':
    fire.Fire(App)
