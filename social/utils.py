from django.db.models import Q


def create_user_search_query(words):
    qs = [Q(username__icontains=word) |
          Q(first_name__icontains=word) |
          Q(last_name__icontains=word) for word in words]
    query = qs.pop()
    # |= is set operator in python
    for q in qs:
        query |= q

    return query
