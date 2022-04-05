import os
import spacy
import scispacy
from scispacy.linking import EntityLinker

from scispacy.linking_utils import KnowledgeBase
from scispacy.candidate_generation import DEFAULT_PATHS, DEFAULT_KNOWLEDGE_BASES
from scispacy.candidate_generation import (
    CandidateGenerator,
    LinkerPaths
)


FBBT_JSON = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../resources/fbbt-cedar.jsonl")
nmslib_index = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../linker/nmslib_index.bin")
concept_aliases = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../linker/concept_aliases.json")
tfidf_vectorizer = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../linker/tfidf_vectorizer.joblib")
tfidf_vectors_sparse = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../linker/tfidf_vectors_sparse.npz")


CustomLinkerPaths_FBBT = LinkerPaths(
    ann_index=nmslib_index,
    tfidf_vectorizer=tfidf_vectorizer,
    tfidf_vectors=tfidf_vectors_sparse,
    concept_aliases_list=concept_aliases
)


class FBBTKnowledgeBase(KnowledgeBase):
    def __init__(
        self,
        file_path: str = FBBT_JSON,
    ):
        super().__init__(file_path)


# Admittedly this is a bit of a hack, because we are mutating a global object.
# However, it's just a kind of registry, so maybe it's ok.
DEFAULT_PATHS["fbbt"] = CustomLinkerPaths_FBBT
DEFAULT_KNOWLEDGE_BASES["fbbt"] = FBBTKnowledgeBase

linker = CandidateGenerator(name="fbbt")

nlp = spacy.load("en_core_sci_sm")
nlp.add_pipe("scispacy_linker", config={"resolve_abbreviations": True, "linker_name": "fbbt", "threshold": 0.85})

sentence = "The metameric furrows and MesEc that forms between segments during embryonic stage 11 and persists to the " \
           "larval stage (Campos-Ortega and Hartenstein, 1985). Any tracheal lateral trunk anterior branch primordium " \
           "(FBbt:00000234) that is part of some metathoracic tracheal primordium (FBbt:00000188)."
doc = nlp(sentence)
# doc = nlp("Spinal and bulbar muscular atrophy (SBMA) is an \
#            inherited motor neuron disease caused by the expansion \
#            of a polyglutamine tract within the androgen receptor (AR). \
#            SBMA can be caused by this easily.")

words = sentence.split(" ")
for ent in doc.ents:
    # if ent._.kb_ents:
        print("Mention : " + ent.text)
        for fbbt_ent in ent._.kb_ents:
            print("----------")
            print(fbbt_ent)
            print(linker.kb.cui_to_entity[fbbt_ent[0]])
        print("********")

