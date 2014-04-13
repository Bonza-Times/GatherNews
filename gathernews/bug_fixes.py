
class v1_bugs:
    """ Any functions that must be called to keep the versions compatible"""

    def fix_create_table_bug(self):
        """ Fix the create table bug

        In GatherNews 0.1.0, a bug was introduced that does not allow you
        to add new RSS feeds to the 'feeds_list.txt' after your initial
        call of the create_tables() method.

        This method was created because we have no way of knowing which
        RSS feed links match which RSS table names without making a call
        to each RSS feed and recreating each table name.

        If you have previously used GatherNews 0.1.0 you should call this
        method once before calling any other methods on your previously
        created 'FeedMe.db'. Once this method is called then the issue should
        be resolved.

        Returns:
            Writes a JSON object to your disk called 'previous_feeds_list'
            that will fix the create_table() bug.

        Raises:
            UserWarning: This bug fix is not needed
        """
        
        # get table names from the database
        db_names = self.get_tablenames()

        # get table names from RSS feeds
        create_these_tables = {}
        for RSS_link in self.read_file(self.path, "feeds_list.txt"):
            d = feedparser.parse(RSS_link)
            table_name = re.sub(r'\W+', '', d.feed.title)
            create_these_tables[table_name] = RSS_link

        # see if the links associated with the table names are already here
        path = self.path
        file_name = 'previous_feeds_list.json'
        with open(path + file_name, 'r') as f:
            current_backup = json.load(f)

        count = 0
        backup_count = len(current_backup) 
        for name in create_these_tables.keys():
            if create_these_tables[name] in current_backup:
                count += 1
                
        if count == backup_count:
            # Warn the user that this bug fix is not needed
            raise UserWarning("This bug fix is not needed")

        else:
                
            # see which names match
            correct_RSS_links = []
            for table in db_names:
                if table in create_these_tables:
                    correct_RSS_links.append(create_these_tables[table])
                elif table not in db_names:
                    print table, " was not found in feeds_list.txt'"

            # Write the JSON object to disk
            with open(path + 'previous_feeds_list.json',
                      mode = 'w') as f:
                return json.dump(correct_RSS_links, f)
