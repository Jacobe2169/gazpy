# coding = utf-8
import warnings

def is_number(x):
    return (isinstance(x,float) or isinstance(x,int))

class QueryBuilder():
    """

    """

    def __init__(self):
        """Constructor for QueryBuilder"""
        pass

    def query(self,**kwargs):
        #Query Type
        term=kwargs.get("term",False)
        query_string = kwargs.get("query_string", False)
        nested = kwargs.get("nested", False)
        match_all=kwargs.get("match_all",False)

        #Value
        value=kwargs.get("value","")

        # Additional Filter
        sorted = kwargs.get("sorted", False)
        regexped = kwargs.get("regexp", False)
        sized  = kwargs.get("sized", False)
        min_valued = kwargs.get("min_valued", False)
        max_valued = kwargs.get("max_valued", False)
        in_radius= kwargs.get("in_radius",False)

        # Additional Filter Value
        field = kwargs.get("field", "")
        nested_field = kwargs.get("nested_field", "")
        sorted_by = kwargs.get("sorted_by", "")
        size = kwargs.get("size", 1)
        min_value = kwargs.get("min_value", 0)
        max_value = kwargs.get("max_value", 2000000)
        radius_size = kwargs.get("radius_size", 1)
        radius_unit = kwargs.get("radius_unit", "km")
        radius_centroid=kwargs.get("radius_centroid",(0,0))
        regexp_value = kwargs.get("regexp_value", "")
        geo_field=kwargs.get("geo_field","coord")


        if match_all and (query_string or term or nested):
            raise Exception("Match all can't be combine with other queries!")
        if term and query_string:
            raise Exception("Impossible to have term and query_string at the same time")

        if nested and (not isinstance(nested_field,str) or not nested_field):
            raise Exception("You forgot to indicate the nested_field name !")

        if regexped and term:
            raise Exception("You can't use regexp with term query")

        if (not field and not match_all) or not isinstance(field,str) :
            raise Exception("Missing field name or bad type!")

        if not self.check_consistency(sorted,regexped,sized,min_valued,max_valued,in_radius,
                          sorted_by,size,min_value,max_value,radius_size,radius_unit,regexp_value,geo_field):
            raise Exception("Args of query() are not consistent! Double Check!")

        body_query={
            "query":{}
        }


        if query_string:
            body_query["query"]={"query_string":{"default_field":field,"query":value if not regexped else regexp_value}}
        elif term:
            body_query["query"]={"term":{field:value}}
        elif match_all:
            body_query["query"] = {"match_all":{}}

        body_query["query"]={"bool":{"must":[body_query["query"]]}}

        if min_valued:
            body_query["query"]["bool"]["must"].append({"range": {"gt": min_value}})
        if max_valued:
            body_query["query"]["bool"]["must"].append({"range": {"lt": max_value}})

        if in_radius:
            body_query["query"]["bool"]["filter"]={"geo_distance":{"distance":"{0}{1}".format(radius_size,radius_unit),geo_field:{"lon":radius_centroid[0],"lat":radius_centroid[1]}}}

        if nested:
            if query_string:
                body_query["query"]["bool"]["must"][0]["query_string"]["default_field"]=".".join([field,nested_field])
            elif term:
                body_query["query"]["bool"]["must"][0]= {"term":{".".join([field,nested_field]):value}}

            body_query["query"]={"nested":{"path":field,"query":body_query["query"]}}

        if sorted:
            body_query["sort"]=[{sorted_by:"desc"}]
        if sized:
            body_query["size"]=size
        return body_query

    def check_consistency(self,sorted,regexped,sized,min_valued,max_valued,in_radius,
                          sorted_by,size,min_value,max_value,radius_size,radius_unit,regexp_value,geo_field):

        if sorted and (not isinstance(sorted_by,str) or not sorted_by):
            warnings.warn("sorted_by must not be an empty and should be a str")
            return False

        if sized and (not is_number(size) or not size):
            warnings.warn("sorted_by must not be an empty and should be a str")
            return False

        if min_valued and (not is_number(min_value) or not min_value):
            warnings.warn("sorted_by must not be an empty and should be a str")
            return False

        if max_valued and (not is_number(max_value) or not max_value):
            warnings.warn("sorted_by must not be an empty and should be a str")
            return False

        if in_radius and (not isinstance(geo_field,str) or not is_number(radius_size) or not isinstance(radius_unit,str) or not radius_unit or not radius_size or not geo_field):
            warnings.warn("sorted_by must not be an empty and should be a str")
            return False

        if regexped and (not isinstance(regexp_value,str) or not regexp_value):
            warnings.warn("sorted_by must not be an empty and should be a str")
            return False

        return True


def test_consistency():
    pass