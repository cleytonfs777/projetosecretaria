let categorias = {
    "noone": [
        ["noone", "Nenhum"]
    ],
    "pg": [
        ["noone", "Nenhum"],
        ["sd2cl", "Sd 2ª Classe BM"],
        ["sd", "Sd BM"],
        ["cb", "Cb BM"],
        ["3sgt", "3º Sgt BM"],
        ["2sgt", "2º Sgt BM"],
        ["1sgt", "1º Sgt BM"],
        ["subten", "Sub Ten BM"],
        ["2ten", "2º Ten BM"],
        ["1ten", "1º Ten BM"],
        ["cap", "Cap BM"],
        ["maj", "Maj BM"],
        ["tencel", "Ten Cel BM"],
        ["cel", "Cel BM"]
    ],
    "loc": [
        ["noone", "Nenhum"],
        ['acf', 'ACF'],
        ['acf1', 'ACF-1'],
        ['acf2', 'ACF-2'],
        ['acf3', 'ACF-3'],
        ['sdts1', 'SDTS-1'],
        ['sdts2', 'SDTS-2'],
        ['sdts3', 'SDTS-3'],
        ['nts', 'NTS'],
        ['gol', 'GOL'],
        ['sdal', 'SDAL'],
        ['sdal1', 'SDAL-1'],
        ['sdal2', 'SDAL-2'],
        ['sdal3', 'SDAL-3'],
        ['sdal4', 'SDAL-4'],
        ['secretaria', 'Secretaria'],
    ],
    "num_emp": [
        ["noone", "Nenhum"],
        ["max_emp", "Mais Emp"],
        ["min_emp", "Menos Emp"]
    ],
    "num_hti": [
        ["noone", "Nenhum"],
        ["max_hti", "Mais H Típ"],
        ["min_hti", "Menos H Típ"]
    ],
    "num_hat": [
        ["noone", "Nenhum"],
        ["max_hat", "Mais H Atíp"],
        ["min_hat", "Menos H Atíp"]
    ]
}



console.log(JSON.stringify(categorias))
console.log(categorias.num_hat[0][1])