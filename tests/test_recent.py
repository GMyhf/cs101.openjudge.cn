"""Recent additions use first catalog dates, calendar windows, and visibility rules."""
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import server

ROOT = Path(__file__).resolve().parents[1]


class RecentDatesTests(unittest.TestCase):
    def test_summary_uses_record_dates_and_history_without_exposing_private_books(self):
        rows = [
            {'book': 'practice', 'id': '1', 'test_count': 1},
            {'book': 'practice', 'id': '2', 'test_count': 1, 'added_at': '2026-10-18'},
            {'book': 'practice', 'id': '3', 'test_count': 0},
            {'book': 'private', 'id': '1000000', 'test_count': 1},
        ]
        with tempfile.TemporaryDirectory() as directory:
            mirror = Path(directory)
            (mirror / 'added_dates.json').write_text(json.dumps({
                'practice/1': '2026-10-09', 'practice/2': '2026-10-01',
                'private/1000000': '2026-10-10',
            }))
            with patch.object(server, 'MIRROR', mirror), patch.object(server, 'catalog_raw', return_value={'problems': rows}), patch.object(server, 'catalog_title', return_value='题目'):
                payload = server.visible_catalog(server.catalog_summary_payload(), '')
                self.assertEqual([p['added_at'] for p in payload['problems']], ['2026-10-09', '2026-10-18'])
                self.assertNotIn('private', payload['book_meta'])
                (mirror / 'added_dates.json').unlink()
                payload = server.catalog_summary_payload()
                self.assertEqual(payload['problems'][0]['added_at'], '')
                self.assertEqual(payload['problems'][1]['added_at'], '2026-10-18')

    def test_history_covers_current_catalog(self):
        dates = json.loads((ROOT / 'data/openjudge/added_dates.json').read_text())
        rows = json.loads((ROOT / 'data/openjudge/catalog.json').read_text())['problems']
        for row in rows:
            key = f"{row['book']}/{row['id']}"
            self.assertRegex(row.get('added_at') or dates.get(key, ''), r'^\d{4}-\d{2}-\d{2}$', key)

    @unittest.skipUnless(shutil.which('node'), 'node unavailable')
    def test_calendar_ranges_filters_and_rendering(self):
        script = r'''
const fs = require('fs'), vm = require('vm'), assert = require('assert');
const elements = new Map();
const get = key => {
  if (!elements.has(key)) elements.set(key, {hidden: true, textContent:'', innerHTML:''});
  return elements.get(key);
};
const buttons = ['10','30','3m','all'].map(range => ({dataset:{range}, setAttribute(k,v){this[k]=v}, addEventListener(k,f){this.click=f}}));
const data = {today:'2026-10-18', problems:[
 {book:'practice',id:'1',title:'1: 新题',path:'/practice/1/',added_at:'2026-10-18'},
 {book:'practice',id:'2',title:'边界',path:'/practice/2/',added_at:'2026-10-09'},
 {book:'practice',id:'3',title:'更早',path:'/practice/3/',added_at:'2026-10-08'},
 {book:'practice',id:'4',title:'旧题',path:'/practice/4/',added_at:'2026-07-17'},
 {book:'practice',id:'5',title:'无日期',path:'/practice/5/',added_at:''},
 {book:'practice',id:'6',title:'<script>',path:'/practice/6/',added_at:'2026-10-10'},
 {book:'2024fallroutine',id:'7',title:'隐藏题库',path:'/2024fallroutine/7/',added_at:'2026-10-18'},
 {book:'practice',id:'8',title:'未来',path:'/practice/8/',added_at:'2026-10-19'}
]};
const context = vm.createContext({URL,URLSearchParams,location:{href:'https://example.test/recent/',search:''},history:{replaceState(){}},document:{querySelector:get,querySelectorAll:()=>buttons},fetch:async()=>({ok:true,json:async()=>data})});
vm.runInContext(fs.readFileSync('static/recent.js','utf8'),context);
assert.equal(context.recentStart('2026-10-18','10'),'2026-10-09');
assert.equal(context.recentStart('2026-10-18','30'),'2026-09-19');
assert.equal(context.recentStart('2026-05-31','3m'),'2026-02-28');
assert.equal(context.recentStart('2024-05-31','3m'),'2024-02-29');
setImmediate(()=>{
 assert(get('#count').textContent.includes('4 道'));
 buttons[0].click();
 assert(get('#count').textContent.includes('3 道'));
 assert(!get('#list').innerHTML.includes('隐藏题库'));
 assert(!get('#list').innerHTML.includes('未来'));
 assert(get('#list').innerHTML.includes('&lt;script&gt;'));
 assert(!get('#list').innerHTML.includes('1: 新题'));
 buttons[2].click(); assert(get('#count').textContent.includes('4 道'));
 buttons[3].click(); assert(get('#count').textContent.includes('7 道'));
 assert(get('#list').innerHTML.includes('日期未记录'));
 vm.runInContext('problems=[];render()',context);
 assert(!get('#empty').hidden); assert(get('#list').hidden);
});
'''
        result = subprocess.run(['node', '-e', script], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
