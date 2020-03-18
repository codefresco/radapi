#
from flask import url_for

class PaginationMixin(object):
    @staticmethod
    def collect(query, page, limit, endpoint, **kwargs):
        paged= query.paginate(page, limit, False)
        response= {
            'data': [item.packin() for item in paged.items],
            'metadata': {
                        'page': page,
                        'limit': limit,
                        'total_pages': paged.pages,
                        'total_items': paged.total,
                        'links': {
                                    'self': url_for(endpoint, page=page, limit=limit, **kwargs),
                                    'next': url_for(endpoint, page=page + 1, limit=limit, **kwargs) if paged.has_next else None,
                                    'prev': url_for(endpoint, page=page - 1, limit=limit, **kwargs) if paged.has_prev else None
                                  }
                        }
        }
        return response