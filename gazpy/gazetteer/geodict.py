# coding = utf-8


from .base import Base,parse_label,parse_label2

class Geodict(Base):
    """"""

    def __init__(self,es_client):
        """Constructor for Geodict"""
        Base.__init__(self,es_client)

    def get_by_label(self, label, lang, score=True, size=1):
        query=self.qb.query(term=True,field=lang,value=label,sorted=score,sorted_by=self.score_field,sized=True,size=size)
        return self.convert_es_to_pandas(self.es_client.search("gazetteer","place",query))

    def get_by_alias(self, alias, lang, score=True, size=1):
        query = self.qb.query(term=True,nested=True,nested_field=lang,field="aliases", value=alias, sorted=score, sorted_by=self.score_field, sized=True,
                              size=size)
        return self.convert_es_to_pandas(self.es_client.search("gazetteer", "place", query))

    def get_n_label_similar(self, label, lang, n, score=True):
        query = self.qb.query(query_string=True, regexp=True,regexp_value=parse_label2(label,lang), field=lang, value=label, sorted=score,
                              sorted_by=self.score_field, sized=True,
                              size=n)
        return self.convert_es_to_pandas(self.es_client.search("gazetteer", "place", query))

    def get_n_alias_similar(self, alias, lang, n, score=True):
        query = self.qb.query(query_string=True, nested=True, nested_field=lang, regexp=True,regexp_value=parse_label2(alias,lang),field="aliases", value=alias, sorted=score,
                              sorted_by=self.score_field, sized=True,
                              size=n)
        return self.convert_es_to_pandas(self.es_client.search("gazetteer", "place", query))

    def get_in_radius(self, lon, lat, unit="km",distance=10, score=True, size=1):
        query = self.qb.query(match_all=True,in_radius=True,radius_size=distance,radius_unit=unit,radius_centroid=(lon,lat), sorted=score,
                              sorted_by=self.score_field, sized=True,geo_field="coord",
                              size=size)
        return self.convert_es_to_pandas(self.es_client.search("gazetteer", "place", query))

    def get_by_id(self, id):
        query = self.qb.query(term=True, field="id", value=id, sized=True,
                              size=1)
        return self.convert_es_to_pandas(self.es_client.search("gazetteer", "place", query))

    def get_by_other_id(self,id,identifier="wikidata"):
        if not identifier in ['wikidata','geonames']:
            raise Exception("Identfier type must be taken from the following items : 'wikidata' or 'geonames'")
        if identifier == 'wikidata':
            id_field="wikidataID"
        else:
            id_field="geonameID"
        query = self.qb.query(term=True, field=id_field, value=id, sized=True,
                              size=1)
        return self.convert_es_to_pandas(self.es_client.search("gazetteer", "place", query))