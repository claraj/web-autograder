var codeConvert = {
  data: function (code) {

    year = Number(code.slice(0, 4))

    if (!year) { return `${code} unknown`; }

    term = code.slice(4, 6)

    terms = { '01': 'Fall', '03': 'Spring', '05': 'Summer'}

    termString = terms[term]
    if (!termString) { return `${code} unknown`; }

    if (term != '01') {
      year++;
    }

    return `${termString} ${year}`
  }
}
