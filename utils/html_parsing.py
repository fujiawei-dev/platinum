# Licensed to the White Turing under one or more
# contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The SFC licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

'''HTML Parsing'''

from os import remove

from requests_html import HTML


def html_parsing(fp=r'utils/commands.py'):
    remove(fp)
    
    with open(r'html/List of Chromium Command Line Switches « Peter Beverloo.html', encoding='utf-8') as f:
        doc = f.read()

    html = HTML(html=doc)
    condition = html.xpath('//tr/@id')
    explanation = html.xpath('//tr/td[2]/text()')
    
    for i, j in zip(condition, explanation):
        k = i.split('   ')[0].replace("'", '').replace('-', '_').replace('.', '_').upper()
        if len(k) < 1 or not k[0].isalpha():
            continue
        print(f'{k} = {i.strip()!r}   # {j.strip()}', file=open(fp, 'a', encoding='utf-8'))


if __name__ == '__main__':
    html_parsing()
