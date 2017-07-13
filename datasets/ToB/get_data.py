from glob import glob
import re



def get_proto():
    resres = '<div class="results_record">(.*?)</div><!-- results_record_end -->'
    proto = '<font color="green">Proto-Kiranti:</font></span> <span class="unicode">(.*?)</span>'
    meaning = '<span class="fld">Meaning:</span> <span class="unicode">(.*?)</span>'
    infiles = glob('proto/response*')
    for f in infiles:
        data = open(f).read()
        results = re.findall(resres, data, re.DOTALL)
        for r in results:
            print(re.findall(meaning, r, re.DOTALL),
                re.findall(proto, r, re.DOTALL))
 
def get_language(which):
    resres = '<div class="results_record">(.*?)</div><!-- results_record_end -->'
    proto = '<font color="green">Entry:</font></span> <span class="unicode">(.*?)</span>'

    meaning = '<span class="fld">Meaning:</span> <span class="unicode">(.*?)</span>'
    nepali = '<span class="fld">Nepali:</span> <span class="unicode">(.*?)</span>'
    grammar = '<span class="fld">Grammar:</span> <span class="unicode">(.*?)</span>'
    etymon = 'text_number=(.*?)&root=config" target="_self"><span class="unicode">Kiranti etymology</span></a>'
    
    infiles = glob(which+'/response*')
    out = []
    idx = 1
    for f in infiles:
        data = open(f).read()
        results = re.findall(resres, data, re.DOTALL)

        for i, r in enumerate(results):
            frm = re.findall(proto, r, re.DOTALL) or ['']
            cnc = re.findall(meaning, r, re.DOTALL) or ['']
            nep = re.findall(nepali, r, re.DOTALL) or ['']
            pos = re.findall(grammar, r, re.DOTALL) or ['']
            etm = re.findall(etymon, r, re.DOTALL) or ['']

            if frm:
                print(frm[0], cnc[0], nep[0], pos[0], etm[0])
                out += [[str(idx), which, frm[0], cnc[0], nep[0], pos[0],
                    etm[0].replace('+', '')]]
                idx += 1

    with open(which+'.tsv', 'w') as f:
        f.write('\t'.join([
            'RN', 'DOCULECT', 'REFLEX', 'CONCEPT', 'NEPALI', 'GFN',
            'ETYMON'])+'\n')
        for line in out:
            f.write('\t'.join(line)+'\n')

if __name__ == '__main__':
    from sys import argv
    import os
    get_language(argv[1])
    os.system('/home/mattis/.pythonvenv/bin/stdb coverage -p {0}.tsv --taxon {0}'.format(argv[1])) 
