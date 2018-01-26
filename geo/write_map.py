import geojson
import lingpy as lp
import json

def write_map(varieties, outfile):
    languages = lp.csv2list(varieties)
    colors = ["#a6cee3", "#1f78b4", "#b2df8a", "#33a02c", "#fb9a99", "#e31a1c",
            "#fdbf6f", "#ff7f00", "#cab2d6", "#6a3d9a", '#040404', '#F6E3CE',
            '#81F79F', '#8A0808', '#FA58F4', '#0489B1', '#088A08']
    colors = colors + colors + colors
    points = []
    header = [x.strip() for x in languages[0]]
    nidx = header.index('NAME')
    latidx = header.index('LAT')
    lonidx = header.index('LON')
    #pinidx = header.index('PINYIN')
    #hanidx = header.index('HANZI')
    groupidx = header.index("SUBGROUP")
    #pinidx = header.index("PINYIN")
    #famidx = header.index('FAMILY')

    groups = sorted(set([line[groupidx] for line in languages[1:]]))
    print(len(groups), len(colors), groups)
    for line in languages[1:]:
        name = line[nidx]
        #pinyin = line[pinidx]
        #hanzi = line[hanidx]
        lat, lon = line[latidx], line[lonidx]
        group = line[groupidx]
        #family = line[famidx]
        if lat.strip() and lat != '?':
            lat, lon = float(lat), float(lon)
            if lat > 400 or lon > 400:
                raise ValueError("Coords for {0} are wrong.".format(name))
            point = geojson.Point((lon, lat))
            feature = geojson.Feature(geometry=point, 
                    properties = {
                        #"Family" : family,
                        "Variety" : name,
                        #"Pinyin" : pinyin,
                        #"Chinese" : hanzi,
                        "Group" : group,
                        "marker-color" : colors[groups.index(group)]
                        })
            points += [feature]
    with open(outfile, 'w') as f:
        f.write(json.dumps(geojson.FeatureCollection(points)))

if __name__ == '__main__':

    write_map('languages_yunfan_240118.tsv', 'output.geojson')
