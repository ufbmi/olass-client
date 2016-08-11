"""
Goal: Provides paginate() function
"""
from sqlalchemy import orm
from olass.models.pagination import Pagination


class BaseQuery(orm.Query):
    """
    @see: flask-sqlalchemy/flask_sqlalchemy/__init__.py
    """

    def paginate(self, page=None, per_page=None, error_out=True):
        """Returns ``per_page`` items from page ``page``.

        If no items are found and ``page`` is greater than 1, or if page is
        less than 1, it aborts with 404.  This behavior can be disabled by
        passing ``error_out=False``.

        If ``page`` or ``per_page`` are ``None``, they will default to 1 and 20
        respectively.  If the values are not ints and ``error_out`` is
        ``True``, this function will rais exceptions.

        Returns a :class:`Pagination` object.
        """

        if page is None:
            page = 1

        if per_page is None:
            per_page = 20

        if error_out and page < 1:
            raise Exception("Pagination error: page < 1")

        items = self.limit(per_page).offset(
            (page - 1) * per_page).all()

        if not items and page != 1 and error_out:
            raise Exception("Pagination error: no items and page != 1")

        # No need to count if we're on the first page and there are fewer
        # items than we expected.
        if page == 1 and len(items) < per_page:
            total = len(items)
        else:
            total = self.order_by(None).count()

        return Pagination(self, page, per_page, total, items)
