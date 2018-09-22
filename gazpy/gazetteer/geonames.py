# coding = utf-8
from .base import Base,parse_label,parse_label2


class Geonames(Base):
    """

    """

    def __init__(self,es_client,score="dem"):
        """Constructor for Geodict"""
        Base.__init__(self,es_client,score_field=score,id_field="geonameid",label_fields="name",alias_fields="alternativenames",coordinates_field="coordinates",class_field="feature_code")

    def get_by_label(self, label, lang, score=True, size=1):
        query=self.qb.query(term=True,field="name",value=label,sorted=score,sorted_by=self.score_field,sized=True,size=size)
        return self.to_element(self.es_client.search("geonames","geoname",query))

    def get_by_alias(self, alias, lang, score=True, size=1):
        query = self.qb.query(term=True,field="alternativenames", value=alias, sorted=score, sorted_by=self.score_field, sized=True,
                              size=size)
        return self.to_element(self.es_client.search("geonames", "geoname", query))

    def get_n_label_similar(self, label, lang, n, score=True):
        query = self.qb.query(query_string=True, regexp=True,regexp_value=parse_label2(label,lang), field="name", value=label, sorted=score,
                              sorted_by=self.score_field, sized=True,
                              size=n)
        return self.to_element(self.es_client.search("geonames", "geoname", query))

    def get_n_alias_similar(self, alias, lang, n, score=True):
        query = self.qb.query(query_string=True, regexp=True,regexp_value=parse_label2(alias,lang),field="alternativenames", value=alias, sorted=score,
                              sorted_by=self.score_field, sized=True,
                              size=n)
        return self.to_element(self.es_client.search("geonames", "geoname", query))

    def get_in_radius(self, lon, lat, unit="km",distance=10, score=True, size=1):
        query = self.qb.query(match_all=True,in_radius=True,radius_size=distance,radius_unit=unit,radius_centroid=(lon,lat), sorted=score,
                              sorted_by=self.score_field, sized=True,geo_field="coordinates",
                              size=size)
        return self.to_element(self.es_client.search("geonames", "geoname", query))

    def get_by_id(self, id):
        query = self.qb.query(term=True, field="geonameid", value=id, sized=True,
                              size=1)
        return self.to_element(self.es_client.search("geonames", "geoname", query))

