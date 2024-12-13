''' Module that contains the projects queries '''

def get_all_fields(order_table = None) -> str:
    query = """
        SELECT c.CategoryName, s.Title, art.Name, alb.Title, alb.Year
        FROM Category c, Song s, Artist art, Album alb, IsIn iin, IsOn ion, Plays p
        WHERE c.CategoryID = iin.CategoryID
        AND iin.SongID = s.SongID
        AND p.SongID = s.SongID
        AND p.ArtistID = art.ArtistID
        AND s.SongID = ion.SongID
        AND ion.AlbumID = alb.AlbumID
        """

    if order_table is None: return query + ";"

    match (order_table):
        case 'Category': 
            return query + "ORDER BY c.CategoryName"
        case 'Song':
            return query + "ORDER BY s.Title"
        case 'Artist':
            return query + "ORDER BY art.Name"
        case 'Album':
            return query + "ORDER BY alb.Title"
        case _:
            return query + ";"

def get_all_songs() -> str:
    query = "SELECT Title FROM Song;"
    return query

def get_all_categories() -> str:
    query = "SELECT CategoryName FROM Category;"
    return query

def get_all_artists() -> str:
    query = """
        SELECT a.Name, COUNT(s.SongID) as Songs
        FROM Artist a
        JOIN Plays p ON a.ArtistID = p.ArtistID
        JOIN Song s ON s.SongID = p.SongID
        GROUP BY a.Name;
        """
    return query

def get_all_albums() -> str:
    query = "SELECT Title, Year FROM Album;"
    return query

def get_artist_songs() -> str:
    # params (ArtistName)
    query = """
        SELECT a.Name, s.Title
        FROM Artist a, Song s, Plays p
        WHERE a.Name = ?
        AND a.ArtistID = p.ArtistID
        AND p.SongID = s.SongID;
        """
    return query

def update_artist_song() -> str:
    # params (ArtistName, SongTitle)
    query = """
        INSERT INTO Plays (ArtistID, SongID)
        Values (
            (SELECT ArtistID FROM Artist WHERE Name = ?),
            (SELECT SongID FROM Song WHERE Title = ?)
        );
        """

    return query

def update_song_category() -> str:
    # params (SongTitle, CategoryName)
    query = """
        INSERT INTO IsIn (CategoryID, SongID)
        VALUES (
            (SELECT CategoryID FROM Category WHERE CategoryName = ?),
            (SELECT SongID FROM Song WHERE Title = ?)
        );
        """
    return query

def update_song_album() -> str:
    # params (SongTitle, AlbumTitle)
    query = """
        INSERT INTO IsOn (SongID, AlbumID)
        VALUES (
            (SELECT SongID FROM Song s WHERE s.Title = ?),
            (SELECT AlbumID FROM Album a WHERE a.Title = ?)
        );
        """

    return query

def create_new_category() -> str:
    # params (CategoryName)
    query = """
        INSERT INTO Category (CategoryName)
        VALUES (?);
        """

    return query

def create_new_song() -> str:
    # params (SongTitle)
    query = """
        INSERT INTO Song (Title)
        VALUES (?);
        """

    return query

def create_new_artist() -> str:
    # params (Name)
    query = """
        INSERT INTO Artist (Name)
        VALUES (?);
        """

    return query

def create_new_album() -> str:
    # params (Title, Year)
    query = """
        INSERT INTO Album (Title, Year)
        VALUES (?, ?);
        """

    return query

def delete_song() -> str:
    # params (Title)
    query = """
        DELETE FROM Song WHERE Title = ?;
        """

    return query

def delete_album() -> str:
    # params (AlbumTitle)
    query = """
        DELETE FROM Album WHERE Title = ?;
        """

    return query

def delete_artist() -> str:
    # params (ArtistName)
    query = """
        DELETE FROM Artist WHERE Name = ?;
        """

    return query

def delete_category() -> str:
    # params (CategoryName)
    query = """
        DELETE FROM Category WHERE CategoryName = ?;
        """

    return query

