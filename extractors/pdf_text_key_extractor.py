def extract_key_value(key, pdf):

    label = pdf.pq('LTTextLineHorizontal:contains("{0}")'.format(key))
    if label.attr('x0') is None or label.attr('y0') is None:
        return None
    left_corner = float(label.attr('x0'))
    bottom_corner = float(label.attr('y0'))
    value = pdf.pq('LTTextLineHorizontal:in_bbox("%s, %s, %s, %s")' % (
    left_corner, bottom_corner, left_corner + 300, bottom_corner + 15)).text()
    return value
