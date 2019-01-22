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


# Produce platinum/chromium.py
def html_parsing_chromium(fp=r'utils/commands.py'):
    p = """# Licensed to the White Turing under one or more
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

    '''List of Chromium Command Line Switches.'''


    class Chromium(object):
        '''Frequently used commands mappings.
        
        There are lots of command lines which can be used with the Google Chrome browser.
        Some change behavior of features, others are for debugging or experimenting.
        This page lists the available switches including their conditions and descriptions.
        Last update occurred on 2018-06-08 from `https://peter.sh/experiments/chromium-command-line-switches/`.
        '''
    """
    
    remove(fp)
    print(p, file=open(fp, 'a', encoding='utf-8'))

    with open(r'html/List of Chromium Command Line Switches « Peter Beverloo.html', encoding='utf-8') as f:
        doc = f.read()

    html = HTML(html=doc)
    condition = html.xpath('//tr/@id')
    explanation = html.xpath('//tr/td[2]/text()')
    
    for i, j in zip(condition, explanation):
        k = i.split('   ')[0].replace("'", '').replace('-', '_').replace('.', '_').upper()
        j = j.replace('\n', '')
        if len(k) < 1 or not k[0].isalpha():
            continue
        print(f'    {k} = {i.strip()!r}   # {j.strip()}', file=open(fp, 'a', encoding='utf-8'))


# Produce platinum/data/ios.json
# https://en.wikipedia.org/wiki/IOS_version_history
def html_parsing_ios(fp=r'utils/ios.json'):
    import json
    
    with open(r'html/iOS version history - Wikipedia.htm', encoding='utf-8') as f:
        doc = f.read()
        
    html = HTML(html=doc)
    nv = html.xpath('//tr[@valign="top"]/th[not(@colspan)]/text()[1]')[64: -1]
    cv = html.xpath('//tr[@valign="top"]/td[1]/text()[1]')[64:-1]

    nv = map(lambda x: x.strip(), nv)
    cv = map(lambda x: x.strip().split('/')[-1], cv)
    
    json.dump(dict(zip(nv, cv)), fp=open(fp, 'w'))


if __name__ == '__main__':
    # html_parsing_chromium('platinum/chromium.py')
    html_parsing_ios('platinum/data/ios.json')
