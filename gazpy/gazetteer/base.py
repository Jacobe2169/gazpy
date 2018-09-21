# coding = utf-8
from ..query.query_builder import QueryBuilder
import pandas as pd
import re, os ,inspect

from ..objectify import objectify as ob

__geo_res_path=os.path.join(os.path.dirname(inspect.getfile(ob)),"resources/")

geo_term={
    "fr":open(__geo_res_path.rstrip("/")+"/geo_term_fr").read().lower().strip().split("\n"),
    "en":open(__geo_res_path.rstrip("/")+"/geo_term_en").read().strip().split("\n")
}
def parse_label2(label : str,lang):
    if not lang in geo_term:
        return parse_label(label)

    label = re.sub("[ ]+", " ", re.sub('[(?)]+', "", label.strip()))
    label = label.strip("'").strip("’")

    parts=label.split(" ")
    # f=False
    # for part in parts:
    #     if part.lower() in geo_term[lang]:
    #         f=True
    # if not f:
    #     return parse_label(label)
    new_labels=[]
    for part in parts:
        if not part.lower() in geo_term[lang]:
            new_labels.append(parse_label(part).strip("/?")+"+")
        else:
            new_labels.append(parse_label(part).strip("/"))
    return "/"+"[ ]?".join(new_labels)+"/"




def parse_label(label: str):
    """
    Parse label/toponym to a specific regular expression that allows dissimilarity with the official toponyms/aliases.

    Parameters
    ----------
    label : str
        toponym
    Returns
    -------
    str
        regular expression built from the toponym
    """
    label = re.sub("[ ]+", " ", re.sub('[(?)]+', "", label.strip()))
    label = label.strip("'").strip("’")
    new_label = ""
    for c in label:
        if c.isupper():
            close_par = ")" if not (new_label.endswith(")") or new_label.endswith("?")) and new_label != "" else ""
            # if new_label.endswith("]"):
            #     new_label = new_label[:-1] + "({0}{1}]".format(c.lower(), c)
            # else:
            new_label += close_par + "([{0}{1}]".format(c.lower(), c)
            # print("upper", new_label)
        elif c == " ":
            new_label += ")?[ ]?"
            # print("espace", new_label)
        elif c == "'" or c == "’":
            new_label += c + ")?"
            # print("apostrophe", new_label)
        else:

            new_label += ("(" if new_label == "" else "") + ("(" if new_label.endswith("?") else "") + c
            # print("else", new_label)
    new_label = "/" + new_label + ")?/"
    return new_label

class Base():
    """
    Base class for getter
    """

    def __init__(self,es_client,field_score="score"):
        """Constructor for Base"""
        self.score_field=field_score
        self.qb=QueryBuilder()
        self.es_client=es_client

    def get_by_label(self,label,lang,score=True,size=1):
        raise NotImplementedError()

    def get_by_alias(self,alias,lang,score=True,size=1):
        raise NotImplementedError()

    def get_n_label_similar(self,label,lang,n,score=True):
        raise NotImplementedError()

    def get_n_alias_similar(self,alias,lang,n,score=True):
        raise NotImplementedError()

    def get_in_radius(self,lon,lat,score=True,size=1):
        raise NotImplementedError()

    def get_by_id(self,id):
        raise NotImplementedError()

    def convert_es_to_pandas(self,es_query_results):
        """
        Return a `pandas.Dataframe` object built from the elasticsearch query results

        Parameters
        ----------
        es_query_results : dict
            elasticsearch.search() result

        Returns
        -------
        pandas.DataFrame
            Dataframe of the elasticsearch query results
        """
        if es_query_results["hits"]["total"] == 0:
            return None
        df = pd.DataFrame([g["_source"] for g in es_query_results["hits"]["hits"]])
        if self.score_field in df:
            df[self.score_field] = df[self.score_field].apply(lambda x: float(x))
        else:
            df[self.score_field] = df.apply(lambda x: 0)
        df[self.score_field].fillna(-1, inplace=True)
        return df