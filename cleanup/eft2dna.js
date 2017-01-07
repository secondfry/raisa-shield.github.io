var types_by_name = null;

$.getJSON('http://raisa-shield.github.io/_static/types_by_name.json')
    .success(function (data) {
        types_by_name = data;
    });

function eft2dna(ship, data) {
    var lines = data.split('\n'),
        items = {},
        result = types_by_name[ship].id.toString(),
        re = new RegExp('[0-9 ]+x;')
    lines.forEach(function (line) {

        var t = types_by_name[line];
        if (t != undefined) {
            if (items[t.id] == undefined) {
                items[t.id] = 0;
            }
            items[t.id] += 1;
        }
    });
    $.each(items, function (item, q) {
        result += ':' + item.toString() + ';' + q.toString();
    });
    return result + '::';
}
