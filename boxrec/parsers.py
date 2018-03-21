import lxml.html
from .models import Fight, Boxer


class FailedToParse(Exception):
    pass


class BaseParser(object):
    def __init__(self):
        pass

    def make_dom_tree(self, response):
        encoding = response.encoding
        binary_contents = response.content

        lxml_parser = lxml.html.HTMLParser(encoding=response.encoding)
        tree = lxml.html.document_fromstring(
            response.content,
            parser=lxml_parser
        )

        return tree


class FightParser(BaseParser):
    BASE_DOM_PATH = \
        '//div[@class="singleColumn"]//table[@class="responseLessDataTable"]/tr'

    def get_event_and_fight_id(self, url):
        splitted = url.rsplit('/')

        event_id = splitted[-2]
        fight_id = splitted[-1]
        return event_id, fight_id

    def get_boxer_ids(self, tree):
        boxer_links = tree.xpath(
            FightParser.BASE_DOM_PATH + '//a[./img]/@href'
        )

        try:
            left = boxer_links[0].rsplit('/')[-1]
            right = boxer_links[1].rsplit('/')[-1]
        except IndexError:
            raise FailedToParse("Could not get boxers for fight")

        if left == '0' or right == '0':
            raise FailedToParse(
                'Fight is not complete, one of the boxers is TBA'
            )

        return left, right

    def clean_rating(self, raw):
        if raw is None:
            return None

        return int(raw.rsplit('\n')[0].replace(',',''))

    def get_rating_before_fight(self, tree):
        rating_row = tree.xpath(
            FightParser.BASE_DOM_PATH + \
                '[./td/b/text() = "before fight"]/td[position() = 1 or position() =3]'
        )
        rating_left = self.clean_rating(rating_row[0].text)
        rating_right = self.clean_rating(rating_row[1].text)

        return rating_left, rating_right

    def get_rating_after_fight(self, tree):
        """ New function to determine rating after fight."""
        rating_row = tree.xpath(
             FightParser.BASE_DOM_PATH + \
                '[./td/b/text() = "after fight"]/td[position() = 1 or position() =3]'  
        )
        rating_left = self.clean_rating(rating_row[0].text)
        rating_right = self.clean_rating(rating_row[1].text)

        return rating_left, rating_right

    def get_fight_outcome(self, tree, left_id, right_id):
        outcome = tree.xpath(
            FightParser.BASE_DOM_PATH + '//td[./span[@class="textWon"]]/a[./img]/@href'
        )

        try:
            winner_id = outcome[0].rsplit('/')[-1]
        except IndexError as e:
            drawn = tree.xpath(
                FightParser.BASE_DOM_PATH + '//td[./span[@class="textDrawn"]]/a[./img]/@href'
            )
            if len(drawn) > 0:
                return 'drawn'
            else:
                raise FailedToParse('Could not determine fight outcome, did it already occur?')

        if left_id == winner_id:
            return 'left'
        else:
            return 'right'

    def get_stance(self,tree):
        stance_row = tree.xpath(
            FightParser.BASE_DOM_PATH +
                '[./td/b/text() = "stance"]/td[position() = 1 or position() =3]'
        )
        stance_left = stance_row[0].text
        stance_right = stance_row[1].text

        return stance_left, stance_right
        
    def get_age(self,tree):
        age_row = tree.xpath(
            FightParser.BASE_DOM_PATH +
                '[./td/b/text() = "age"]/td[position() = 1 or position() =3]'
        )
        try:
            age_left = age_row[0].text
            age_right = age_row[1].text
        except:
            age_left = 'QQQ'
            age_right = 'QQQ'

        return age_left, age_right

    def get_height(self,tree):
        height_row = tree.xpath(
            FightParser.BASE_DOM_PATH +
                '[./td/b/text() = "height"]/td[position() = 1 or position() =3]'
        )
        try:
            height_left = height_row[0].text.rsplit('/')[1].strip().replace('cm','')
            height_right = height_row[1].text.rsplit('/')[1].strip().replace('cm','')
        except:
            height_left = 'QQQ'
            height_right = 'QQQ'
        
        return height_left, height_right

    def get_reach(self,tree):
        reach_row = tree.xpath(
            FightParser.BASE_DOM_PATH +
                '[./td/b/text() = "reach"]/td[position() = 1 or position() =3]'
        )
        try:
            reach_left = reach_row[0].text.rsplit('/')[1].strip().replace('cm','')
            reach_right = reach_row[1].text.rsplit('/')[1].strip().replace('cm','')
        except:
            reach_left = 'QQQ'
            reach_right = 'QQQ'

        return reach_left, reach_right

    def get_won(self,tree):
        won_row = tree.xpath(
            FightParser.BASE_DOM_PATH +
                '[./td/b/text() = "won"]/td[position() = 1 or position() =3]'
        )
        try:
            won_left = won_row[0].text
            won_right = won_row[1].text
        except:
            won_left = 'QQQ'
            won_right = 'QQQ'

        return won_left, won_right

    def get_lost(self,tree):
        lost_row = tree.xpath(
            FightParser.BASE_DOM_PATH +
                '[./td/b/text() = "lost"]/td[position() = 1 or position() =3]'
        )
        try:
            lost_left = lost_row[0].text
            lost_right = lost_row[1].text
        except:
            lost_left = 'QQQ'
            lost_right = 'QQQ'

        return lost_left, lost_right
        
    def get_drawn(self,tree):
        drawn_row = tree.xpath(
            FightParser.BASE_DOM_PATH +
                '[./td/b/text() = "drawn"]/td[position() = 1 or position() =3]'
        )
        try:
            drawn_left = drawn_row[0].text
            drawn_right = drawn_row[1].text
        except:
            drawn_left = 'QQQ'
            drawn_right = 'QQQ'

        return drawn_left, drawn_right
        
    def get_KO(self,tree):
        KO_row = tree.xpath(
            FightParser.BASE_DOM_PATH +
                '[./td/b/text() = "KOs"]/td[position() = 1 or position() =3]'
        )
        try:
            KO_left = KO_row[0].text
            KO_right = KO_row[1].text
        except:
            KO_left = 'QQQ'
            KO_right = 'QQQ'

        return KO_left, KO_right
        
    def parse(self, response):
        tree = self.make_dom_tree(response)

        event_id, fight_id = self.get_event_and_fight_id(response.url)
        boxer_left_id, boxer_right_id = self.get_boxer_ids(tree)
        rating_before_left, rating_before_right = self.get_rating_before_fight(tree)
        rating_after_left, rating_after_right = self.get_rating_after_fight(tree)
        stance_left, stance_right = self.get_stance(tree)
        age_left, age_right = self.get_age(tree)
        height_left, height_right = self.get_height(tree)
        reach_left, reach_right = self.get_reach(tree)
        won_left, won_right = self.get_won(tree)
        lost_left, lost_right = self.get_lost(tree)
        drawn_left, drawn_right = self.get_drawn(tree)
        KO_left, KO_right = self.get_KO(tree)
        result = self.get_fight_outcome(tree, boxer_left_id, boxer_right_id)

        return Fight(
            event_id=event_id,
            fight_id=fight_id,
            boxer_left_id=boxer_left_id,
            boxer_right_id=boxer_right_id,
            hist_rating_left=rating_before_left,
            hist_rating_right=rating_before_right,
            curr_rating_left=rating_after_left,
            curr_rating_right=rating_after_right,
            stance_left=stance_left,
            stance_right=stance_right,
            age_left=age_left,
            age_right=age_right,
            height_left=height_left,
            height_right=height_right,
            reach_left=reach_left,
            reach_right=reach_right,
            won_left=won_left,
            won_right=won_right,
            drawn_left=drawn_left,
            drawn_right=drawn_right,
            lost_left=lost_left,
            lost_right=lost_right,
            KO_left=KO_left,
            KO_right=KO_right,
            winner=result
        )


class FightListParser(BaseParser):
    BASE_DOM_PATH = \
        '//div[@class="content"]//table[@class="calendarTable"]'

    def get_event_and_fight_ids(self, tree):
        links = tree.xpath(
            FightListParser.BASE_DOM_PATH \
                + '//td[@class="actionCell"]/div[@class="mobileActions"]/a[1]/@href'
        )

        events = map(lambda x: x.rsplit('/')[-2], links)
        fights = map(lambda x: x.rsplit('/')[-1], links)

        return events, fights


    def parse(self, response):
        tree = self.make_dom_tree(response)

        event_ids, fight_ids = \
            self.get_event_and_fight_ids(tree)

        return zip(event_ids, fight_ids)


class BoxerParser(BaseParser):
    BASE_DOM_PATH = \
        '//div[@class="singleColumn"]//table[@class="profileTable"][1]'

    def get_boxer_id(self, url):
        return url.rsplit('/')[-1]

    def get_boxer_name(self, tree):
        return tree.xpath(
            BoxerParser.BASE_DOM_PATH + '//h1/text()'
        )[0]

    def parse(self, response):
        tree = self.make_dom_tree(response)

        boxer_id = self.get_boxer_id(response.url)
        boxer_name = self.get_boxer_name(tree)

        return Boxer(
            id = boxer_id,
            name = boxer_name
        )
