import hashlib

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    DateTime,
    func,
    event
    )
from sqlalchemy.orm import relationship

from .support import db

class Cluster(db.Model):
    """
    A cluster of documents, usually generated by automatic analysis.
    A cluster consists of some metadata and a collection of documents
    within that cluster. A document can be long to many clusters.

    A cluster has a fingerprint, which is an md5 hash of the sorted
    document ids in the cluster. Always call `recalculate_fingerprint`
    after updating the members of the cluster.
    """
    __tablename__ = "clusters"

    id           = Column(Integer, primary_key=True)
    fingerprint  = Column(String(32), index=True, nullable=False, unique=True)
    created_at   = Column(DateTime(timezone=True), index=True, unique=False, nullable=False, server_default=func.now())

    # associations
    # the members of this cluster, instances of ClusteredDocument
    members      = relationship("ClusteredDocument", backref='cluster', cascade='all, delete-orphan', passive_deletes=True)

    @property
    def documents(self):
        return [cd.document for cd in self.members]

    def recalculate_fingerprint(self):
        self.fingerprint = Cluster.make_fingerprint(m.document.id for m in self.members)

    def __len__(self):
        return len(self.members)

    def __repr__(self):
        return "<Cluster id=%s, %d docs, fingerprint=%s>" % (self.id, len(self), self.fingerprint,)

    @classmethod
    def make_fingerprint(cls, doc_ids):
        m = hashlib.md5()
        for i in sorted(doc_ids):
            m.update(str(i))
        return m.hexdigest()

    @classmethod
    def find_or_create(cls, fingerprint=None, docs=None):
        """ Find an existing cluster that has these documents, or create one. """
        if not fingerprint:
            if not docs:
                raise ValueError("Need one of fingerprint or docs")
            fingerprint = cls.make_fingerprint(d.id for d in docs)

        cluster = cls.query.filter(cls.fingerprint == fingerprint).first()
        if cluster is None:
            cluster = cls()
            cluster.members = [ClusteredDocument(document=d) for d in docs]
            cluster.recalculate_fingerprint()

        return cluster


class ClusteredDocument(db.Model):
    """
    Links a document to a cluster.
    """
    __tablename__ = "clustered_documents"

    id         = Column(Integer, primary_key=True)
    cluster_id = Column(Integer, ForeignKey('clusters.id', ondelete='CASCADE'), index=True, nullable=False)
    doc_id     = Column(Integer, ForeignKey('documents.id', ondelete='CASCADE'), index=True, nullable=False)

    # associations
    document   = relationship("Document", backref='clusters', lazy=False)

    def __repr__(self):
        return "<ClusteredDocument id=%s, cluster=%s, document=%s>" % (self.id, self.cluster, self.document,)
