from django import template

register = template.Library()


@register.simple_tag
def get_pagination_range(page_obj, num_pages_display=5):
    paginator = page_obj.paginator
    current = page_obj.number
    last = paginator.num_pages

    left = max(1, current - num_pages_display // 2)
    right = min(last, current + num_pages_display // 2)

    if current - num_pages_display // 2 < 1:
        right = min(last, right + (1 - (current - num_pages_display // 2)))

    if current + num_pages_display // 2 > last:
        left = max(1, left - (current + num_pages_display // 2 - last))

    page_range = list(range(left, right + 1))

    if left > 1:
        page_range.insert(0, '...')
        page_range.insert(0, 1)

    if right < last:
        page_range.append('...')
        page_range.append(last)

    return page_range
