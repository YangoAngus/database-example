from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
import datetime as dt

Base = declarative_base()
engine = create_engine("sqlite://", future=True)


class Bands(Base):
    __tablename__ = "bands"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    add_time = Column(DateTime, default=dt.datetime.now(), nullable=False)

    album = relationship("Albums", back_populates="band")

    def __repr__(self):
        return f"Band: {self.name}, Was add: {self.add_time}"


class Albums(Base):
    __tablename__ = "albums"

    id = Column(Integer, primary_key=True)
    band_id = Column(Integer, ForeignKey("bands.id"), nullable=False)
    name = Column(String(255), nullable=False)
    add_time = Column(DateTime, default=dt.datetime.now(), nullable=False)

    band = relationship("Bands", back_populates="album")

    def __repr__(self):
        return f"Band: {self.band.name} Album: {self.name}"


Base.metadata.create_all(engine)


class Database:

    def __init__(self, session, *args):
        self.BandsTable = args[0] if args[0].__name__ == "Bands" else None
        self.AlbumsTable = args[1] if args[1].__name__ == "Albums" else None
        self.session = session

    def checkIfBandExist(self, band) -> bool:
        if self.session.query(self.BandsTable).filter_by(name=band).first():
            return True
        return False

    def checkIfAlbumExist(self, band_id, album) -> bool:
        if self.session.query(self.AlbumsTable).filter_by(band_id=band_id, name=album).first():
            return True
        return False

    def countBands(self) -> int:
        return self.session.query(self.BandsTable).count()

    def countAlbums(self) -> int:
        return self.session.query(self.AlbumsTable).count()

    def addBand(self, band) -> None:
        self.session.add(self.BandsTable(name=band.lower()))
        self.session.commit()

    def getBandId(self, band) -> int:
        return self.session.query(self.BandsTable).filter_by(name=band).first().id

    def addAlbum(self, band_id, album) -> None:
        self.session.add(self.AlbumsTable(band_id=band_id, name=album.lower()))
        self.session.commit()

    def getAlbumId(self, album) -> int:
        return self.session.query(self.AlbumsTable).filter_by(name=album).first().id

    def bandsNamesOrderByAlphabet(self) -> list:
        return [i.name for i in self.session.query(self.BandsTable).order_by(self.BandsTable.name).all()]

    def bandNamesOrderByAlphabetDesc(self) -> list:
        return [i.name for i in self.session.query(self.BandsTable).order_by(self.BandsTable.name.desc()).all()]

    def albumsNamesOrderByAlphabet(self) -> list:
        return [i.name for i in self.session.query(self.AlbumsTable).order_by(self.AlbumsTable.name).all()]

    def albumsNamesOrderByAlphabetDesc(self) -> list:
        return [i.name for i in self.session.query(self.AlbumsTable).order_by(self.AlbumsTable.name.desc()).all()]

    def bandsAlbumsRelationJson(self) -> dict:
        return {i.name: [a.name for a in self.session.query(self.AlbumsTable).filter_by(band_id=i.id).order_by(
            self.AlbumsTable.name).all()]
                for i in self.session.query(self.BandsTable).order_by(self.BandsTable.name).all()}


if __name__ == "__main__":
    with Session(engine) as s:
        db = Database(s, Bands, Albums)
        if not db.checkIfBandExist('pink floyd'):
            db.addBand('pink floyd')

        if not db.checkIfAlbumExist(db.getBandId('pink floyd'), 'dark side of the moon'):
            db.addAlbum(db.getBandId('pink floyd'), 'dark side of the moon')

        if not db.checkIfAlbumExist(db.getBandId('pink floyd'), 'the wall'):
            db.addAlbum(db.getBandId('pink floyd'), 'the wall')

        if not db.checkIfBandExist('acdc'):
            db.addBand('acdc')

        if not db.checkIfAlbumExist(db.getBandId('acdc'), 'back in black'):
            db.addAlbum(db.getBandId('acdc'), 'back in black')

        if not db.checkIfAlbumExist(db.getBandId('acdc'), 'razor age'):
            db.addAlbum(db.getBandId('acdc'), 'razor age')

        if not db.checkIfBandExist('led zeppelin'):
            db.addBand('led zeppelin')

        if not db.checkIfAlbumExist(db.getBandId('led zeppelin'), 'led zeppelin i'):
            db.addAlbum(db.getBandId('led zeppelin'), 'led zeppelin i')

        if not db.checkIfAlbumExist(db.getBandId('led zeppelin'), 'led zeppelin ii'):
            db.addAlbum(db.getBandId('led zeppelin'), 'led zeppelin ii')

        print('count bands', db.countBands())  # count bands
        print('count albums', db.countAlbums())  # count albums
        print('bands names order by alphabet')
        print(db.bandsNamesOrderByAlphabet())  # bands names order by alphabet
        print('bands names order by alphabet desc')
        print(db.bandNamesOrderByAlphabetDesc())  # bands names order by alphabet desc
        print('albums names order by alphabet')
        print(db.albumsNamesOrderByAlphabet())  # albums names order by alphabet
        print('albums names order by alphabet desc')
        print(db.albumsNamesOrderByAlphabetDesc())  # albums names order by alphabet desc
        print('bands albums json')
        print(db.bandsAlbumsRelationJson())  # bands albums json
