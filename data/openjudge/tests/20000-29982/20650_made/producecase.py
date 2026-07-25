import subprocess, tempfile
from pathlib import Path
CASES=['ABCBDAB\nBDCABA\n', 'CDCDDBCDDACC\nCECEACEDBBAEACCDBE\n', 'CDBEBDADCCDBCCAA\nAEEBDBCBDDDCBBAEEDE\n', 'BAEBCBEEDBDE\nCDAA\n', 'BBAAAABCCADEACAE\nEDBC\n', 'BDCEAD\nEDD\n', 'EBAADEBAABECCDDEBDA\nEDDBBEADBCD\n', 'EBDAACAEEECCBADCBEDE\nBCCCBACEEBABBAEBDCEB\n', 'EBECCEEBCBAD\nCDCDEBEACEEADEAECAED\n', 'EDDBDBAA\nDBBACCABB\n', 'CDCECCBDBAC\nAEEEDBBBA\n', 'DDEEDAADCDBEBD\nAADAAABDCBADC\n', 'BC\nCA\n', 'DCDBDDDEAADA\nAACECBEBACD\n', 'ACEAEEAEECDDBCE\nCBCBDEDACBECACD\n', 'EAD\nEEBDDAECCACDDE\n', 'DCDE\nCBDBA\n', 'DDACDEBAE\nBECABBCCAEDBA\n', 'CCDDECCCB\nCEADADCEC\n', 'DBEEBABDEB\nECDD\n']
SOURCE='def longest_common_subsequence(s1, s2):\n    dp = [[0 for _ in range(len(s2)+1)] for _ in range(len(s1)+1)]\n    for i in range(len(s1)):\n        for j in range(len(s2)):\n            if s1[i] == s2[j]:\n                dp[i+1][j+1] = dp[i][j] + 1\n            else:\n                dp[i+1][j+1] = max(dp[i+1][j], dp[i][j+1])\n    return dp[len(s1)][len(s2)]\n\ns1 = input()\ns2 = input()\nprint(longest_common_subsequence(s1, s2))\n'
with tempfile.NamedTemporaryFile('w',suffix='.py') as f:
 f.write(SOURCE); f.flush()
 root=Path(__file__).parent/'data'
 for i,c in enumerate(CASES):
  o=subprocess.run(['python3',f.name],input=c,text=True,capture_output=True,check=True).stdout
  (root/f'{i}.in').write_text(c); (root/f'{i}.out').write_text(o)
