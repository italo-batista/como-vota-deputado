import datetime as dt

import comovotadeputado.opendata.controller as open_dt_ctrl
from comovotadeputado.cache import cache
from comovotadeputado.cache.constants import CacheConstants, CachePrefixesKeys


class AttendancesCtrl:

    def get_all_attendances_date_dataframe(self, day, month, year, **kwargs):
        cache_key = CachePrefixesKeys.ALL_ATTENDANCES_DATE_PREFIXE_KEY + str(day) + str(month) + str(year) + \
                    kwargs["congressperson_id"] + kwargs["political_party_initials"] + kwargs["uf_initials"]

        @cache.cache(cache_key, expire=CacheConstants.EXPIRATION_TIME)
        def _get_all_attendances_date_dataframe(day, month, year, **kwargs):
            date = dt.datetime(year, month, day)
            attendances_df = open_dt_ctrl.get_attendances_dataframe(date, **kwargs)
            return attendances_df

        return _get_all_attendances_date_dataframe(day=day, month=month, year=year, **kwargs)
