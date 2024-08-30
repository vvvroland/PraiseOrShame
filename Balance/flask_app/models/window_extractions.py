from flask_app.config.mysqlconnection import connect_to_mysql
from flask_app import stuffing
from flask import flash
from flask_app.models import user_extractions



class Praise:
    def __init__(self,data):
        self.id=data["id"]
        self.sun=data["sun"]
        self.public=data["public"]
        self.liker=data["liker"]
        self.created_at=data["created_at"]
        self.updated_at=data["updated_at"]
        self.userpr_id=data["userpr_id"]
        self.users = []
        self.soother = None

    @classmethod
    def get_all_praise(cls):
        query = """
            SELECT * FROM praise LEFT JOIN users ON praise.userpr_id = users.id;
            """
        results = connect_to_mysql(stuffing).query_db(query)
        all_praise = []
        if results:
                for row in results:
                    this_praise =cls(row)
                    user_data = {
                        **row,
                        'id': row['users.id'],
                    'created_at': row['users.created_at'],
                    'updated_at': row['users.updated_at'],
                    }
                    this_user = user_extractions.Users(user_data)
                    this_praise.soother = this_user
                    all_praise.append(this_praise)
        return all_praise
    
    @classmethod
    def get_all_praise_public(cls):
        query = """
            SELECT * FROM praise LEFT JOIN users ON praise.userpr_id = users.id WHERE praise.public=1;
            """
        results = connect_to_mysql(stuffing).query_db(query)
        public_praise = []
        if results:
                for row in results:
                    this_praise =cls(row)
                    user_data = {
                        **row,
                        'id': row['users.id'],
                    'created_at': row['users.created_at'],
                    'updated_at': row['users.updated_at'],
                    }
                    this_user = user_extractions.Users(user_data)
                    this_praise.soother = this_user
                    public_praise.append(this_praise)
        return public_praise
    
    
    @classmethod
    def get_all_praise_public_by_id(cls,data):
        query = """
            SELECT * FROM praise LEFT JOIN users ON praise.userpr_id = users.id WHERE praise.public=1 and users.id=%(id)s;
            """
        results = connect_to_mysql(stuffing).query_db(query,data)
        your_public_praise = []
        if results:
                for row in results:
                    these_praise =cls(row)
                    user_data = {
                        **row,
                        'id': row['users.id'],
                    'created_at': row['users.created_at'],
                    'updated_at': row['users.updated_at'],
                    }
                    these_user = user_extractions.Users(user_data)
                    these_praise.soother = these_user
                    your_public_praise.append(these_praise)
                    print(these_praise)
        return your_public_praise
    
    
    @classmethod
    def get_all_praise_public_api(cls):
        query = """
            SELECT praise.id, sun, liker, userpr_id FROM praise LEFT JOIN users ON praise.userpr_id = users.id WHERE praise.public=1;
            """
        results = connect_to_mysql(stuffing).query_db(query)                
        return results
    

    @classmethod
    def get_all_praise_private(cls):
        query = """
            SELECT * FROM praise LEFT JOIN users ON praise.userpr_id = users.id WHERE praise.public=0;
            """
        results = connect_to_mysql(stuffing).query_db(query)
        private_praise = []
        if results:
                for row in results:
                    this_praise =cls(row)
                    user_data = {
                        **row,
                        'id': row['users.id'],
                    'created_at': row['users.created_at'],
                    'updated_at': row['users.updated_at'],
                    }
                    this_user = user_extractions.Users(user_data)
                    this_praise.soother = this_user
                    private_praise.append(this_praise)
        return private_praise

    
    @classmethod
    def get_all_praise_private_by_id(cls,data):
        query = """
            SELECT * FROM praise LEFT JOIN users ON praise.userpr_id = users.id WHERE praise.public=0 and users.id=%(id)s;
            """
        results = connect_to_mysql(stuffing).query_db(query,data)
        your_private_praise = []
        if results:
                for row in results:
                    these_praise =cls(row)
                    user_data = {
                        **row,
                        'id': row['users.id'],
                    'created_at': row['users.created_at'],
                    'updated_at': row['users.updated_at'],
                    }
                    these_user = user_extractions.Users(user_data)
                    these_praise.soother = these_user
                    your_private_praise.append(these_praise)
        return your_private_praise

    @classmethod
    def add_like_praise_api(cls, data):
        query = """
            UPDATE praise SET
            liker = liker + 1
            WHERE praise.id = %(id)s;
            """
        print(data)
        return connect_to_mysql(stuffing).query_db(query,data)

    @classmethod
    def add_like_praise(cls, data):
        query = """
            UPDATE praise SET
            liker = liker + 1
            WHERE praise.id = %(id)s;
            """
        print(data)
        return connect_to_mysql(stuffing).query_db(query,data)

    @classmethod
    def get_by_id_praise(cls,data):
        query = """SELECT * from praise JOIN users ON users.id = praise.userpr_id WHERE praise.id=%(id)s;"""
        results = connect_to_mysql(stuffing).query_db(query,data) 
        if results:
            whole_praise = cls(results[0])
            #if questions, print this row to see where the thing is going.
            single=results[0]
            #     return whole_praise every praise has a user
            user_data={
                **single,
                'id': single['users.id'],
                'created_at': single['users.created_at'],
                'updated_at': single['users.updated_at']
            }
            this_user = user_extractions.Users(user_data)
            whole_praise.soother = this_user
            return whole_praise
        return False
    
    @classmethod
    def update_praise(cls, data):
        query = """
            UPDATE praise SET
            sun = %(sun)s,
            public= %(public)s
            WHERE praise.id = %(id)s;
        """
        return connect_to_mysql(stuffing).query_db(query,data)

    @classmethod
    def add_praise(cls,data):
        query="""INSERT INTO praise (sun,public,userpr_id)
            VALUES(%(sun)s,%(public)s, %(userpr_id)s);"""
        results = connect_to_mysql(stuffing).query_db(query,data)
        print(results)
        return results

    @classmethod
    def delete_praise(cls, data):
        query = """
            DELETE FROM praise WHERE praise.id = %(id)s;
        """
        return connect_to_mysql(stuffing).query_db(query,data)



    @staticmethod
    def valid_praise(data):
        is_valid =True
        if len(data['sun'])<1:
            is_valid = False
            flash('You cannot submit an empty praise')
        elif len(data['sun'])<7:
            is_valid = False
            flash('Praise must be at least 3 characters long',)
        if "public" not in data:
            is_valid = False
            flash('You must indicate whether the praise is public or private')
        return is_valid





class Shame:
    def __init__(self,data):
        self.id=data["id"]
        self.shade=data["shade"]
        self.public=data["public"]
        self.liker=data["liker"]
        self.created_at=data["created_at"]
        self.updated_at=data["updated_at"]
        self.usersh_id=data["usersh_id"]
        self.users = []
        self.stinger = None

    @classmethod
    def get_all_shame(cls):
        query = """
            SELECT * FROM shame LEFT JOIN users ON shame.usersh_id = users.id;
            """
        results = connect_to_mysql(stuffing).query_db(query)
        all_shame = []
        if results:
                for row in results:
                    this_shame =cls(row)
                    user_data = {
                        **row,
                        'id': row['users.id'],
                    'created_at': row['users.created_at'],
                    'updated_at': row['users.updated_at'],
                    }
                    that_user = user_extractions.Users(user_data)
                    this_shame.stinger = that_user
                    all_shame.append(this_shame)
        return all_shame
    


    @classmethod
    def get_all_shame_public(cls):
        query = """
            SELECT * FROM shame LEFT JOIN users ON shame.usersh_id = users.id WHERE shame.public=1;
            """
        results = connect_to_mysql(stuffing).query_db(query)
        public_shame = []
        if results:
                for row in results:
                    this_shame =cls(row)
                    user_data = {
                        **row,
                        'id': row['users.id'],
                    'created_at': row['users.created_at'],
                    'updated_at': row['users.updated_at'],
                    }
                    that_user = user_extractions.Users(user_data)
                    this_shame.stinger = that_user
                    public_shame.append(this_shame)
        return public_shame
    
        
    @classmethod
    def get_all_shame_public_by_id(cls,data):
        query = """
            SELECT * FROM shame LEFT JOIN users ON shame.usersh_id = users.id WHERE shame.public=1 and users.id=%(id)s;
            """
        results = connect_to_mysql(stuffing).query_db(query,data)
        your_public_shame = []
        if results:
                for row in results:
                    these_shame =cls(row)
                    user_data = {
                        **row,
                        'id': row['users.id'],
                    'created_at': row['users.created_at'],
                    'updated_at': row['users.updated_at'],
                    }
                    these_user = user_extractions.Users(user_data)
                    these_shame.soother = these_user
                    your_public_shame.append(these_shame)
        return your_public_shame
    

    @classmethod
    def get_all_shame_public_api(cls):
        query = """
            SELECT shame.id, shade, liker, usersh_id FROM shame LEFT JOIN users ON shame.usersh_id = users.id WHERE shame.public=1;
            """
        results = connect_to_mysql(stuffing).query_db(query)                
        return results

    @classmethod
    def get_all_shame_private(cls):
        query = """
            SELECT * FROM shame LEFT JOIN users ON shame.usersh_id = users.id WHERE shame.public=0;
            """
        results = connect_to_mysql(stuffing).query_db(query)
        private_shame = []
        if results:
                for row in results:
                    this_shame =cls(row)
                    user_data = {
                        **row,
                        'id': row['users.id'],
                    'created_at': row['users.created_at'],
                    'updated_at': row['users.updated_at'],
                    }
                    that_user = user_extractions.Users(user_data)
                    this_shame.stinger = that_user
                    private_shame.append(this_shame)
        return private_shame
        
    @classmethod
    def get_all_shame_private_by_id(cls,data):
        query = """
            SELECT * FROM shame LEFT JOIN users ON shame.usersh_id = users.id WHERE shame.public=0 and users.id=%(id)s;
            """
        results = connect_to_mysql(stuffing).query_db(query,data)
        your_private_shame = []
        if results:
                for row in results:
                    these_shame =cls(row)
                    user_data = {
                        **row,
                        'id': row['users.id'],
                    'created_at': row['users.created_at'],
                    'updated_at': row['users.updated_at'],
                    }
                    these_user = user_extractions.Users(user_data)
                    these_shame.soother = these_user
                    your_private_shame.append(these_shame)
        return your_private_shame
    

    @classmethod
    def add_like_shame_api(cls, data):
        query = """
            UPDATE shame SET
            liker = liker + 1
            WHERE shame.id = %(id)s;
            """
        print(data)
        return connect_to_mysql(stuffing).query_db(query,data)
    
    @classmethod
    def add_like_shame(cls, data):
        query = """
            UPDATE shame SET
            liker = liker + 1
            WHERE shame.id = %(id)s;
            """
        print(data)
        return connect_to_mysql(stuffing).query_db(query,data)
    
    @classmethod
    def get_by_id_shame(cls,data):
        query = """SELECT * from shame JOIN users ON users.id = shame.usersh_id WHERE shame.id=%(id)s;"""
        results = connect_to_mysql(stuffing).query_db(query,data) 
        if results:
            whole_shame = cls(results[0])
            #if questions, print this row to see where the thing is going.
            single=results[0]
            #     return whole_praise every praise has a user
            user_data={
                **single,
                'id': single['users.id'],
                'created_at': single['users.created_at'],
                'updated_at': single['users.updated_at']
            }
            this_user = user_extractions.Users(user_data)
            whole_shame.stinger = this_user
            return whole_shame
        return False

    @classmethod
    def update_shame(cls, data):
        query = """
            UPDATE shame SET
            shade = %(shade)s,
            public= %(public)s
            WHERE shame.id = %(id)s;
        """
        return connect_to_mysql(stuffing).query_db(query,data)
    

    @classmethod
    def add_shame(cls,data):
        query="""INSERT INTO shame (shade,public,usersh_id)
            VALUES(%(shade)s,%(public)s, %(usersh_id)s);"""
        results = connect_to_mysql(stuffing).query_db(query,data)
        return results

    @classmethod
    def delete_shame(cls, data):
        query = """
            DELETE FROM shame WHERE shame.id = %(id)s;
        """
        return connect_to_mysql(stuffing).query_db(query,data)




    @staticmethod
    def valid_shame(data):
        is_valid =True
        if len(data['shade'])<1:
            is_valid = False
            flash('You cannot submit an empty shame')
        elif len(data['shade'])<7:
            is_valid = False
            flash('Shame must be at least 7 characters',)
        if "public" not in data:
            is_valid = False
            flash('You must indicate whether the shame is public or private')
        return is_valid