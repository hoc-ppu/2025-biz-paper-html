#!/usr/bin/env python3

from datetime import datetime
from pathlib import Path
# import re
import sys

from lxml import html  # type: ignore
from lxml.html import Element  # type: ignore

import Python_Resources.html_chunk_tool_cmd_with_class_warning as script

table_markup = """<table class="table table-bordered">
  <thead class="thead-light"><tr><th scope="col">Date</th><th scope="col">Original files</th><th scope="col">New files</th></tr></thead>
  <tbody></tbody>
</table>"""

path_to_index_file = '/Users/mark/projects/business-papers/index.html'

existing_base_url = 'https://publications.parliament.uk/pa/cm5801/cmagenda/'

def main():

    # we can except a list of files
    file_paths = sys.argv[1:]

    # also create a table
    html_table = html.fromstring(table_markup)

    for input_file in file_paths:

        # get the sitting_date from the filename
        file_name = Path(input_file).name

        sitting_date = datetime.strptime(file_name, 'OP%y%m%d.html').strftime('%Y-%m-%d')

        creation_date = datetime.now().strftime('%Y-%m-%d')

        # print(sitting_date, creation_date)


        script.DATES.set_up(creation_date, sitting_date)
        input_root = script.massarge_input_file(input_file)
        script.split_and_output(input_root, '/Users/mark/projects/business-papers/new_op_template.html', input_file, output_folder='/Users/mark/projects/business-papers/newHTML')

        ob = file_name.replace('OP', 'ob').replace('.html', '.htm')
        an = file_name.replace('OP', 'an').replace('.html', '.htm')
        fb = file_name.replace('OP', 'fb').replace('.html', '.htm')


        new_ob_filename = f'new_{ob}l'
        new_fb_filename = f'new_{fb}l'

        new_ob_html_filepath = '/newHTML/' + new_ob_filename
        new_fb_html_filepath = '/newHTML/' + new_fb_filename

        row_markup = ('<tr><td>'
                      + script.DATES.sitting_date_long
                      + '</td><td>'
                      f'<a href="{existing_base_url}{ob}">{ob}</a><br/>'
                      f'<a href="{existing_base_url}{an}">{an}</a><br/>'
                      f'<a href="{existing_base_url}{fb}">{fb}</a><br/>'
                      '</td><td>'
                      f'<a href="{new_ob_html_filepath}">{new_ob_filename}</a><br/>'
                      f'<a href="{new_fb_html_filepath}">{new_fb_filename}</a><br/>'
                      '</td></tr>')

        tbody = html_table.find('tbody')
        tbody.append(html.fromstring(row_markup))


    # put the new table in the write place
    html_tree = html.parse(path_to_index_file)
    html_root = html_tree.getroot()

    div = html_root.xpath('//div[@id="op-before-after"]')[0]
    # remove any existing tables
    for table in div.iterfind('table'):
        div.remove(table)
    div.append(html_table)

    html_tree.write(path_to_index_file,
                    doctype='<!DOCTYPE html>',
                    encoding='UTF-8',
                    method="html",
                    xml_declaration=False)



if __name__ == "__main__": main()
