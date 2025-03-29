CREATE SEQUENCE blog_post_id_seq
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1;


CREATE TABLE IF NOT EXISTS blog_post
(
    id integer NOT NULL DEFAULT nextval('blog_post_id_seq'::regclass),
    author_id integer NOT NULL,
    image_id integer,
    html text COLLATE pg_catalog."default" NOT NULL,
    summary text COLLATE pg_catalog."default" NOT NULL,
    title text COLLATE pg_catalog."default" NOT NULL,
    date timestamp without time zone NOT NULL,
    CONSTRAINT blog_post_pkey PRIMARY KEY (id),
    CONSTRAINT blog_post_author_id_fkey FOREIGN KEY (author_id)
        REFERENCES player (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT blog_post_image_id_fkey FOREIGN KEY (image_id)
        REFERENCES public.image (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
);

--- 2016 posts
WITH images AS (
	INSERT INTO image (url) VALUES ('https://image-store.fly.storage.tigris.dev/posts/launch.jpg')
	RETURNING id as image_id
)
INSERT INTO blog_post (author_id, title, summary, html, image_id, date)
SELECT
		(SELECT id FROM player WHERE email ilike 'dallas.fraser.waterloo@gmail.com') AS AuthorId,
		'Launch',
		'Today we launch the official MLSB website!. Stay up to date with scores around the league. This is your home for everything you need to stay up to date with all your baseball info.',
		'
			<p>Get ready MLSBer''s!!! Today we launch the official MLSB website! This is your home for everything you need to stay up to date with all your baseball info. Do you need to plan you lame no fun study time for the term? Do you need to plan your extended raging cottage weekend this summer? We gotch you! With your team’s full game schedule for the term (excluding the best Fridays of your life aka tournaments). Did you just watch a bearded fourth year swat five dings and you’re interested in seeing where he ranks in the league in homeruns? Check out the Sleeman Slugger rankings and Sapporo Singles ranking for the girls.</p>
			<p>
			If you have any issues with the site, find any spelling mistakes or misinformation, or have any general feedback regarding the site, feel free to send us an email at <a href="mailto:convenors@mlsb.info?Subject=MLSB%20Website">scores@mlsb.ca</a>. I’ll be as quick as possible to respond and am more than willing to make functional or aesthetic changes if people would like things moved around.
	
			Enjoy!
			</p>
		',
		images.image_id,
		'2016-04-16'
FROM images;

WITH images AS (
	INSERT INTO image (url) VALUES ('https://image-store.fly.storage.tigris.dev/posts/mlsb-bot.jpg')
	RETURNING id as image_id
)
INSERT INTO blog_post (author_id, title, summary, html, image_id, date)
SELECT
		(SELECT id FROM player WHERE email ilike 'dallas.fraser.waterloo@gmail.com') AS AuthorId,
		'MLSB Bot',
		'This summer MLSB is excited to introduce the MLSB bot: your knees stop ship to everything MLSB. You''ll get game day updates, tournament blasts, even check the lineup for the summers sweetest events and order food from some...',
		'
		<p>
        	This summer MLSB is excited to introduce the MLSB bot: your knees stop ship to everything MLSB. You''ll get game day updates, tournament blasts, even check the lineup for the summers sweetest events and order food from some of your favourite sponsors all from the palm of your hand.

	        Stay connected to your team and everything MLSB this summer using the <a href="http://kik.me/mlsbbot" target="_blank">MLSB bot</a>.
    	</p>
		',
		images.image_id,
		'2016-05-07'
FROM images;

WITH images AS (
	INSERT INTO image (url) VALUES ('https://image-store.fly.storage.tigris.dev/posts/catch.jpg')
	RETURNING id as image_id
)
INSERT INTO blog_post (author_id, title, summary, html, image_id, date)
SELECT
		(SELECT id FROM player WHERE email ilike 'dallas.fraser.waterloo@gmail.com') AS AuthorId,
		'Vince & JP - Fired up!',
		'Hey playas, time for the first player feature of the summer - introducing JP and Vince of Morty''s Magenta.  Although it''s only been a month, these two have made their mark on MLSB. They''ve definitely made up for lost time, seeing as they didn''t get their shit together for last summers league....',
		'
		<p>
        	Hey playas, time for the first player feature of the summer - introducing JP and Vince of Morty''s Magenta.  Although it''s only been a month, these two have made their mark on MLSB. They''ve definitely made up for lost time, seeing as they didn''t get their shit together for last summers league.
    	<p>
        	<img src="https://image-store.fly.storage.tigris.dev/posts/vince.jpg"  alt="Vince" class="postImage" style="">
    	<p>
        	JP has been chosen to be featured for his heroic performance during baseball one Wednesday night. JP managed to skillfully steal home, a rarity in the WNL, bringing his team to victory. Although this did not get him on the Sleeman Sluggers list, this great feat will be talked about for many summers to come. 
    	</p>
    	<p>
        	Vince has become notorious for his skills in the outfield. He has been to known to rob many young men from potential home runs, and even sending some of them home in tears. Pictured above is one of the many, graceful diving catches made by Vince. Rumour has it that he did not actually make that catch, however his dedication to the "diving-only catches" lifestyle is greatly admired.
    	</p>
    	<p>
        	If you see these two around, don''t be afraid to fill up their drink, and show them some MLSB fun before they have to graduate!
    	</p>
		',
		images.image_id,
		'2016-06-09'
FROM images;

WITH images AS (
	INSERT INTO image (url) VALUES ('https://image-store.fly.storage.tigris.dev/posts/rory.png')
	RETURNING id as image_id
)
INSERT INTO blog_post (author_id, title, summary, html, image_id, date)
SELECT
		(SELECT id FROM player WHERE email ilike 'ellu6790@mylaurier.ca') AS AuthorId,
		'Rory',
		'Hi friends, for the remainder of the summer we will be bringing you weekly wrap ups of the action that took place on the field and player feature(s) to keep you entertained. Player Feature - Rory ''Gramps'' Landy...',
		'
			<p> Hi friends, for the remainder of the summer we will be bringing you weekly wrap ups of the action that took place on the field and player feature(s) to keep you entertained. </p>
			<h5><strong>Player Feature - Rory ''Gramps'' Landy</strong></h5> 
			<p>First of all, we are honoured to have a survivor from the first world war in our league, thank you for your service Private Landy. Our first player feature is on former convenor, Rory ''Gramps'' Landy. He''s usually available for autographs at the early bird special at Applebee''s on a Friday afternoon or causing a ruckus at his weekly bingo games along with his old age home friends (pictured below).</p>
			<p>If you''ve heard his (stupid) walkup song for Sportzone, you''d know he''s a devout Ireland fan, but despite his beer touting, binge drinking, puke spewing reputation, he also has a sensitive side. He really only has one weakness on the ball field: dog. If you ever really wanted to distract him on the diamond get a puppy to walk by and he''ll be preoccupied by his exploding ovaries. We''ve been told this is a desirable trait in some ladies so do you gramps, do you.</p>
			<p>Rory has graced us with his presence over 8, 9.... 10 years? Were not really sure, it''s just a long time. After his years of service for 18 different teams you''d think he''d be slowing down… well you''re right. BUT despite the ole bones not being what they used to be, and his memory loss making him forget which side he hits on, he''s still one of the most feared hitters in the league, and we''re confident he could last another 10 years before the school finally realizes he''s using his grandson''s ID to fake his way on and he''s forced into retirement.</p>
			<p><strong>Here are some of his stats:</strong></br>Home runs - SportZone 14 </br>Home runs - TEAMLTD 4 </br>Number of bases ran to on ground balls - 0 (The osteoporosis in his knees is setting in) </br>Number of balls hit to LF - 0 </br>24s bought - 3 </br></p>
			<h4>Weekly Wrap up - June 19-25</h4>
			<p>We are just past the halfway point of the MLSB season and so far we have seen it all, from diving catches to Nick "Kraft Deaner" Deane hitting his first ever home run. As the playoff push intensifies teams are starting to get into a groove and putting up some big numbers in both beers consumed and runs scored.</p>
			<h5><strong>Monday/Wednesday League</strong></h5>
			<p>Kik Kryptonite captained by the one and only Faustino Chilumbo vs Shoeless Sapphire captained by the keg stand champion Ayah Shahrari. It was a hard fought battle but Kik Kryptonite flexed their muscles and came out on topp 17-5. </p>
			<p>Sleeman Saffron and Menchies Mint pulled off a large upsets against Wilfs Wave and Kik Kryptonite respectively. </p>
			<p>SportZone Pink and Pabst Platinum continued their dominance atop the division in anticipation of next week''s matchup of undefeated teams.</p>
			<p>Chainsaw Chocolate continuing its run as the best third year team out there beating Chainsaw Chili.</p>
			<h5><strong>Tuesday/Thursday League</strong></h5>
			<p>The matchup of the week for the Tues/Thurs league was Pabst Blue against RWB Red. Two behemoths clashed and neither fell as it ended in a tie. PITCHER CHUG OFF?!</p>
			<p>Spitz Cyan swept their games this week in their case for the running of best third year team.</p>
			<p>Frat Burger Flamingo and Caliburger Kiwi had what we believe was the lowest scoring game in MLSB history at 2-1... stellar defence on full display. </p>
			
			<h4>Conclusion</h4>
			<p>Stay tuned weekly for more player features and weekly wrap-ups. Cheers no-down!
			- Mitch n'' Shaves AKA Dad n'' Daddy. whichever you prefer</p>
		',
		images.image_id,
		'2016-06-29'
FROM images;

WITH images AS (
	INSERT INTO image (url) VALUES ('https://image-store.fly.storage.tigris.dev/posts/ladies.jpg')
	RETURNING id as image_id
)
INSERT INTO blog_post (author_id, title, summary, html, image_id, date)
SELECT
		(SELECT id FROM player WHERE email ilike 'ellu6790@mylaurier.ca') AS AuthorId,
		'Ladies',
		'Hola nos amigos! (We''re pretty excited about passing spanish). This week''s player feature is a tad late because Mitchell''s mom just got married and was unable to plan around our schedule (selfish) and he just got back. He also wouldn''t let me do the full write up without his supervision....rude. ANYWAY, this is dedicated to our dear, sweet friends, Gillian Geremia, Jenna Furguiele, Joanna Christopolous, and Katrina Litsos... aka the MOPPheads...',
		'
			<p>
				Hola nos amigos! (We''re pretty excited about passing spanish). This week''s player feature is a tad late because Mitchell''s mom just got married and was unable to plan around our schedule (selfish) and he just got back. He also wouldn''t let me do the full write up without his supervision....rude. ANYWAY, this is dedicated to our dear, sweet friends, Gillian Geremia, Jenna Furguiele, Joanna Christopolous, and Katrina Litsos... aka the MOPPheads. 
			</p>
			<p>
				Gillian definitely is the powerhouse of the group with a grand total of 1 double. 1 wind-assisted double. 1 hurricane-summoned-by-the-will-of-God-assisted double. She also has an astounding 1 catch in right field with her glove the size of someone''s bare hand... so that''s actually pretty impressive.
			</p>
			
			<p>
			As rumours go, Joanna was drafted onto the team to tutor her teammates in el espanol. Considering we passed, she passed. Considering we got 50''s on our final exam... she owes us years of our life back after we drank our livers off in celebration. As far as her softball skills go, she''s at the topp of her game... as in she''s exceptionally average, but that doesn''t stop her dancing in the dugout.
			</p>
			
			<p>
			Jenna... uh... Jenna tries... really hard... moving on.
			</p>
			
			<p>
			Katrina is arguably the most valuable asset of the group... and we use the term "valuable" quite generously. She has a catching percentage at second base of about 100%... ironically if you switch those digits around you also get her ground ball percentage (for you math wizards thats 001%). 
			</p>
		',
		images.image_id,
		'2016-07-13'
FROM images;

WITH images AS (
	INSERT INTO image (url) VALUES ('https://image-store.fly.storage.tigris.dev/posts/champs.jpg')
	RETURNING id as image_id
)
INSERT INTO blog_post (author_id, title, summary, html, image_id, date)
SELECT
		(SELECT id FROM player WHERE email ilike 'ellu6790@mylaurier.ca') AS AuthorId,
		'Season Round Up',
		'Last Friday MSLB held the third of four tournaments and it saw some alumni come back for a taste of past glory. They looked a bit rusty (a lot) but they eased that pain with some wobbly pops. In the top division SportZone Pink continued their dominant streak winning their third straight tournament. The final game was a close one with <strong>Claudia Vanderholst</strong> walking it off with a single down the third base line against Pabst Blue...',
		'
			<p>Last Friday MSLB held the third of four tournaments and it saw some alumni come back for a taste of past glory. They looked a bit rusty (a lot) but they eased that pain with some wobbly pops. In the top division SportZone Pink continued their dominant streak winning their third straight tournament. The final game was a close one with <strong>Claudia Vanderholst</strong> walking it off with a single down the third base line against Pabst Blue. In the fourth year division Stark and Perri merged with Mel''s Mauve to cruise to a title. In the third year division Chainsaw Chocolate merged with Morty''s Magenta and came out on top. Congratulations!</p>
			<p>As the final week dawns over us, the playoff race is heating up and teams are vying for position. With make up games set to take place this week along with the last tournament of the year there is lots of softball to play. </p>
			<p>In the <strong>Monday/Wednesday</strong> league the race for the playoffs is as tight as it has ever been, two wins separates 3rd and 8th with Sleeman Saffron on the outside looking in. Anything can happen. Let''s take a quick look at everyone''s remaining schedule. </p>
			<ol>
			    <li>SportZone Pink (19-0-0) - (LazSoc Snow, Mel''s Mauve, and Chainsaw Chilli)</li>
			    <li>Pabst Platinum (18-1-0) -  (Shoeless Sapphire, Freshii Field, and Chainsaw Choco)</li>
			    <li>Veritas Teal (13-5-1) - (Crossroads Crimson, Morty''s Magenta, and Shoeless Sapphire)</li>
			    <li>Chainsaw Chilli (13-5-1) - (Menchies Mint, Shoeless Sapphire, and Sportzone Pink)</li>
			    <li>Wilfs Wave (13-6-0) - (Freshii Flame, Chainsaw Choco, and Tilt Tan)</li>
			    <li>Chainsaw Chocolate (13-6-0) - (Taco Farm, Wilfs Wave, Pabst Platinum)</li>
			    <li>Shoeless Sapphire (12-7-0) - (Pabst Platinum, Chainsaw Chilli, and Veritas Teal)</li>
			    <li>Kik Kryptonite (11-7-1) - (Collins Barrow Blossom, Tilt Tan, and Morty''s Magenta)</li>
			    <hr>
			    <li>Sleeman Saffron (10-9-0) - (Mel''s Mauve, Menchies Mint, and Crossroads Crimson)</li>
			    <li>Morty''s Magenta (9-8-2) - (Tilt Tan, Veritas Teal, and Kik Kryptonite)</li>
			</ol>
			<p>
			    Shoeless Sapphire arguably has the toughest schedule of the bunch but we all know captain Ayah Sharari is holding a team meeting rallying up the troops for a huge week ahead, while Nick Deaner is cooking up some Nic(keys) to success for his squad. Sleeman Saffron has three games against non-playoff teams and will look to take advantage and book their ticket to the big dance.
			</p>
			
			<p>
			In the <strong>Tuesday/Thursday</strong> league things are lot more interesting throughout the standings with races for virtually every spot. Jack Daniels Dark is on the outside looking in but were once favourites to top the league. The last week is sure to be drama packed. Let''s take a look at the remaining schedules:     
			</p>
			
			<ol>
			    <li>Pabst Blue (15-0-4) - (Frat Burger Flamingo, TEAMLTD, and Heaven Honey)</li>
			    <li>RWB Red (15-3-2) - (The Pub on King Pineapple and LazSoc Lime)</li>
			    <li>Menchies Magenta (14-4-1) - (TEAMLTD and Taco Farm Forest)</li>
			    <li>TEAMLTD Denim (14-5-0) - (Menchies Magenta, Pabst Blue and Gino''s Jade)</li>
			    <li>Spitz Cyan (14-6-0) - (Smoke''s Steel and CaliBurger Kiwi)</li>
			    <li>Frat Burger Flamingo (13-5-2) - (Pabst Blue and Smoke''s Steel)</li>
			    <li>Gino''s Jade (12-6-1) - (CaliBurger Kiwi, TEAMLTD and Shoeless Sand)</li>
			    <li>Stark and Perri Cherry (11-7-1) - (Turret Tangerine, Night School Navy and Sleeman Saffron)</li>
			    <hr>
			    <li>Jack Daniels Dark (11-8-1) - (Frat Burger Bronze and Turret Tangerine)</li>
			    <li>Frat Burger Bronze (10-9-1) - (Jack Daniels Dark and Night School Navy)</li>
			</ol>
			
			<p>
			TEAMLTD has the toughest schedule with two games agaisnt top 3 teams on Tuesday but will look to have a big day and skyrocket up the standings. Pabst Blue looks to remain undefeated and top the division. Stark and Perri have a favourable schedule with a game in hand on JD Dark as they look to lock up the last spot in the playoffs. 
			</p>
		',
		images.image_id,
		'2016-07-13'
FROM images;


--- 2022 posts
WITH images AS (
	INSERT INTO image (url) VALUES ('https://image-store.fly.storage.tigris.dev/posts/base-runners.png')
	RETURNING id as image_id
)
INSERT INTO blog_post (author_id, title, summary, html, image_id, date)
SELECT
		(SELECT id FROM player WHERE email ilike 'dallas.fraser.waterloo@gmail.com') AS AuthorId,
		'Batting App',
		'Announcing a new feature for MLSB and MLSB-Alumni. It will allow captains to keep track of everyone stats on their team. This will hopefully allows those great hitters who don''t hit homeruns to highlight their skills...',
		'
			<h3>Batting App - Keep track of stats</h3>
			<p>
			    Announcing a new feature for MLSB and MLSB-Alumni. It will allow captains to keep track of everyone stats on their team.
			    This will hopefully allows those great hitters who don''t hit homeruns to highlight their skills. Captains can still submit their game summaries as before but now have the option of keeping track of the whole game.
			    
			    The feature is available to captains under their profile as "Batting App"
			    <br>
			    <img src="https://image-store.fly.storage.tigris.dev/posts/batting-feature.png"  class="postImage">
			</p>
			    
			<h4>
			    Set your roster
			</h4>
			<p>
			    Once you select the game you want to keep track off you need to first set the order of your lineup.
			    Use the up and down arrows you can re-adjust the order of the lineup.
			    If you need to remove a player you simple need to click on the X next to their name.
			    The app will load your previous used roster to help make things easier for you.
			    Currently there is not support for substitute players.
			    <br>
			    <img src="https://image-store.fly.storage.tigris.dev/posts/setting-roster.png"  class="postImage">
			</p>
			<h4>
			    Tracking Game
			</h4>
			<p>
			    After your roster is set you can proceed to select one the batting options.
			    <ul>
			        <li>S - Single: batter made it to first base and there were no outs</li>
			        <li>SS - Sapporo Single: eligible batter hit ball to grass</li>
			        <li>D - Double: batter made it to second base and there were no outs</li>
			        <li>T - Triple: batter made it to third base and there were no outs</li>
			        <li>HR - Home-run: batter made it around the bases and there were no outs</li>
			        <li>E - Error: batter made it to a base but a fielder made an error on the play</li>
			        <li>SF - Sacrifice-fly: batter hit the ball far enough for runner on third to make it home. Batter is out</li>
			        <li>FC - Fielder''s choice: Fieler choose to get out runner instead of batter</li>
			        <li>FO - Fly-out: Batter hit ball but it was caught</li>
			        <li>GO - Ground-out: Batter hit on the ground and thrown out at first</li>
			        <li>K - Strike-out: Batter strike-out at the plate</li>
			        <li>Auto-out - due to league rules the team needs to take an auto-out</li>
			        <li>Skip - Skip the current batter</li>
			        <li>Undo - undo the previous bat</li>
			    </ul>
			    <br>
			    <img src="https://image-store.fly.storage.tigris.dev/posts/batting-options.png"  class="postImage">
			</p>
			<h4>
			    Runners on base
			</h4>
			<p>
			    The app has a outline of the bases and keeps tracks of runners on base.
			    The app will attempt to move runners forward but sometimes runners are able to take extra bases or sometimes they get thrown out.
			    <br>
			    <strong>
			        Advancing runner:
			    </strong>
			    <br>
			    To advance a runner click the green arrow next to the base they are on.
			    <br>
			    <strong>
			        Running gets out:
			    </strong>
			    <br>
			    If the runners gets out due to a lead-off or a fielder''s choice just click the red X next to the base they are on.
			    The same option could be used for double plays.
			    <br>
			</p>
			<h4>
			    End of a Inning
			</h4>
			<p>
			    Once you there is three outs in a inning the bases will be cleared and the next inning will start.
			</p>
		',
		images.image_id,
		'2022-07-12'
FROM images;

--- 2023 posts
WITH images AS (
	INSERT INTO image (url) VALUES ('https://image-store.fly.storage.tigris.dev/posts/chicago-beers.png')
	RETURNING id as image_id
)
INSERT INTO blog_post (author_id, title, summary, html, image_id, date)
SELECT
		(SELECT id FROM player WHERE email ilike 'dallas.fraser.waterloo@gmail.com') AS AuthorId,
		'Alumni Tournament - July 22nd, 2023',
		'The weather is starting to warm up and soon enough Waterloo Park will be buzzing again. All of MLSB is officially back again this summer and the includes MLSB Alumni. It is more than just a tournament but a full weekend packed with softball, beer and good times...',
		'
			<p>
			    The weather is starting to warm up and soon enough Waterloo Park will be buzzing again. All of MLSB is <strong>officially back again</strong> this summer and the includes MLSB Alumni. 
			    It is more than just a tournament but a full weekend packed with <strong>softball, beer and good times</strong>. People have been known to call in sick on Monday.
			</p>
			<p>
			    For those who miss the cracking the old bat on WP2 you are in luck. MLSB Alumni is the tournament for you.
			    Or are you a cocky fourth year captain who wants to see how your <i>"legendary team"</i> stacks up versus previous year teams.
			    <strong>All current and past teams</strong> are welcome to sign up.
			</p>
			<p>
			    Anyone interested in a putting in a team please send an email to <a href="mailto:mlsbalumni@gmail.com">mlsbalumni@gmail.com</a>. The deadline to register is <strong>June 15th</strong>.
			</p>
			<br>
			<br>
 
			<center>
			    <h4>
			        Here is a teaser for those who are interested:
			    </h4>
			    <iframe
			        class="mobile-video"
			        width="560"
			        height="315"
			        src="https://www.youtube.com/embed/U1gtaSGBuGU"
			        frameborder="0"
			        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
			        allowfullscreen
			        title="MLSB Alumni">
			    </iframe>
			</center>
		',
		images.image_id,
		'2023-04-21'
FROM images;

WITH images AS (
	INSERT INTO image (url) VALUES ('https://image-store.fly.storage.tigris.dev/posts/waterloo-park-construction.png')
	RETURNING id as image_id
)
INSERT INTO blog_post (author_id, title, summary, html, image_id, date)
SELECT
		(SELECT id FROM player WHERE email ilike 'dallas.fraser.waterloo@gmail.com') AS AuthorId,
		'Waterloo Park Construction',
		'Summer is here and so is the construction. It looks like our Waterloo Park will be affected. In particular Diamond 1 will be affected....',
		'
			<p>
			    Summer is here and so is the construction. It looks like our Waterloo Park will be affected. In particular Diamond 1 will be affected.
			</p>
			<br>
			<ul>
			    <li>
			        Parking will not be available at the Bauer Lot for the duration of the season. Alternate parking locations include the Diamond Lot, Silver Lake Lot, Erb Lot, and Seagram Lot.
			    </li>
			    <li>
			        There will be a pedestrian detour from Father David Bauer Drive on the west side of the Operations Building. Pedestrian access on the east side of the Operations Building will be blocked by construction fencing.
			    </li>
			    <li>
			        Diamond 1 dugout gates will be accessible for the whole season, apart from 2-3 weeks when Diamond 1 will be accessible via the equipment gate only.
			    </li>
			    <li>
			        Diamond 1 bleachers will not be available.
			    </li>
			    <li>
			        Any foul balls landing in the construction area will not be retrievable. They will be returned to staff in the Operations Building and can be picked up the following day.
			    </li>
			</ul>
		',
		images.image_id,
		'2023-05-01'
FROM images;

WITH images AS (
	INSERT INTO image (url) VALUES ('https://image-store.fly.storage.tigris.dev/posts/mlsb_alumni.png')
	RETURNING id as image_id
)
INSERT INTO blog_post (author_id, title, summary, html, image_id, date)
SELECT
		(SELECT id FROM player WHERE email ilike 'dallas.fraser.waterloo@gmail.com') AS AuthorId,
		'One hell of a summer',
		'Summer is here and so is the construction. It looks like our Waterloo Park will be affected. In particular Diamond 1 will be affected....',
		'
			<p>
			    Sadly, summer is coming to end. MLSB took a huge step forward this summer with the league growing to 50 teams.
			    The league added some hot new events with <strong>Bingemans Waterpark</strong> and <strong>Kentucky Derby</strong>.
			    Every event seem to sell out instantly.
			    Multiple leage records were broken with top 3 all-time homeruns coming from this year!
			    Congrats to Curtis, Aaron and Brennan.
			    The league may to to start drug testing moving forward because those boys were <strong>straight up juicing</strong>.
			</p>
			<center>
			    <img src="https://image-store.fly.storage.tigris.dev/posts/kentuck_derby.png"  alt="Kentucky Derby" class="postImage">
			</center>
			<br>
			<br>
			<p>
			    Congrats to the winning team <strong>Crank Lite Red</strong>. That is one championship that will make your parents proud!
			    They didnt have the best regular season but they showed that anyone got a chance if they can make it to the dance.
			</p>
			<center>
			    <img src="https://image-store.fly.storage.tigris.dev/posts/crank.png"  alt="Champions" class="postImage">
			</center>
			<br>
			<br>
			<p>
			    Finally, <strong>Gen Z</strong> pumped the old millenials at MLSB Alumni tournament. This year convenor team took home the trophy.
			    For any graduating students make sure to fill out <strong><a href="https://forms.gle/ruRz9Cs9FAHMbch86" target="_blank">this form</a></strong> if you are interested in next year tournament!
			</p>
		',
		images.image_id,
		'2023-08-15'
FROM images;

--- 2024 Post
WITH images AS (
	INSERT INTO image (url) VALUES ('https://image-store.fly.storage.tigris.dev/posts/mlsb-alumni.jpg')
	RETURNING id as image_id
)
INSERT INTO blog_post (author_id, title, summary, html, image_id, date)
SELECT
		(SELECT id FROM player WHERE email ilike 'dallas.fraser.waterloo@gmail.com') AS AuthorId,
		'MLSB Alumni - July 20th, 2024',
		'The weather is starting to warm up and soon enough Waterloo Park will be buzzing again. All of MLSB is officially back again this summer and the includes MLSB Alumni. It is more than just a tournament but a full weekend packed with softball, beer and good times. People have been known to call in sick on Monday....',
		'
			<h3>Alumni back again - July 20th</h3>
			<p>
			    The weather is starting to warm up and soon enough Waterloo Park will be buzzing again. All of MLSB is <strong>officially back again</strong> this summer and the includes MLSB Alumni. 
			    It is more than just a tournament but a full weekend packed with <strong>softball, beer and good times</strong>. People have been known to call in sick on Monday.
			</p>
			<p>
			    For those who miss the cracking the old bat on WP2 you are in luck. MLSB Alumni is the tournament for you.
			    Or are you a cocky fourth year captain who wants to see how your <i>"legendary team"</i> stacks up versus previous year teams.
			    <strong>All current and past teams</strong> are welcome to sign up.
			</p>
			<p>
			    Anyone interested in a putting in a team or just playing either:
			    <ul>
			        <li>please send an email to <a href="mailto:mlsbalumni@gmail.com">mlsbalumni@gmail.com</a></li>
			        <li>
			            Fill out this <a href="https://docs.google.com/forms/d/e/1FAIpQLSc5Qik2ryKT69DJ_YZrScMvY--GuK_kWksUUuXiO4iMQXZmug/viewform?usp=sf_link" target="_blank">form</a>
			        </li>
			    </ul>
			    
			    The deadline to register is <strong>June 1st</strong>.
			</p>
			<br>
			<br>
			
			    
			<center>
			    <h4>
			        Here is a teaser for those who are interested:
			    </h4>
			    <iframe
			        class="mobile-video"
			        width="560"
			        height="315"
			        src="https://www.youtube.com/embed/rJ3QV1iqt2o?si=2jjWadfQ3DdU7ooy"
			        frameborder="0"
			        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
			        allowfullscreen
			        title="MLSB Alumni">
			    </iframe>
			</center>
		',
		images.image_id,
		'2024-02-11'
FROM images;

WITH images AS (
	INSERT INTO image (url) VALUES ('https://image-store.fly.storage.tigris.dev/posts/sportszone-2016.jpg')
	RETURNING id as image_id
)
INSERT INTO blog_post (author_id, title, summary, html, image_id, date)
SELECT
		(SELECT id FROM player WHERE email ilike 'dallas.fraser.waterloo@gmail.com') AS AuthorId,
		'MLSB Hall of Fame',
		'The website was created 8 years ago. Since then, there have been <strong>4497 players, 2684 games and 6014 home runs hit</strong>. Over 80 sponsors have stepped up to help keep the league going. A total of "1696 fun" has been had 🍺!...',
		'
			<p>
			    The website was created 8 years ago.
			    Since then, there have been <strong>4497 players, 2684 games and 6014 home runs hit</strong>.
			    Over 80 sponsors have stepped up to help keep the league going.
			    A total of "1696 fun" has been had 🍺!
			</p>
			<p>
			    By special request, the MLSB <a href="https://mlsb.ca/website/hall-of-fame/2024">hall-of-fame</a> has been added.
			    It ranks the best players and the best teams to have ever played.
			</p>
			<h4 class="mt-2">
			    Sleeman Sluggers
			</h4>
			<p>
			    <strong>No one is touching</strong> <a href="https://mlsb.ca/website/player/2024/345">Jack Romano</a> on the career homerun list.
			    A double degree who put up double-digit homeruns 💣 for 5 different teams from 2016 to 2018.
			    It will be a tough record for anyone to touch unless they play three years or just a shit ton of MLSB Alumni Tournaments (yeah they still count).
			</p>
			<center>
			    <img src="https://image-store.fly.storage.tigris.dev/posts/all-time-great.jpg""  alt="All-time homerun leader" class="postImage">
			</center>
			<p>
			    2023 was a good season for homeruns.
			    <a href="https://mlsb.ca/website/player/2024/4604">Curtis McCully</a> won a tight homerun race with <a href="https://mlsb.ca/website/player/2024/4168">Aaron McConnell</a> and clinched the all-time best season for homeruns with 31.
			    Someone will have to have a hell of a season to ever beat that record.
			</p>
			
			<h4 class="mt-2">
			    Sapporo Singles
			</h4>
			<p>
			    Nothing is more controversial than the Sapporo Singles category.
			    Especially in 2022 when the rulings of Sapporo Singles shifted and it inflated the numbers.
			    It is no coincidence that all the single season leaders are from 2022.
			    It is like the <strong>Steroid Era</strong> of the MLSB.
			    However, great players still find a way to climb to the top and <a href="https://mlsb.ca/website/player/2024/1818">Kim Gubbels</a> still sits on top of the career Sapporo Singles.
			</p>
			
			<h4 class="mt-2">
			    Team Rankings
			</h4>
			<p>
			    Of the <strong>300 teams</strong> to have played, one is at the top of the rankings and that is the <a href="https://mlsb.ca/website/teams/2024/12">2016 SportZone</a>.
			    The team won every game played, including league play, playoffs and 4 tournaments.
			    This team dominated by averaging 21 runs a game and hitting 164 homeruns.
			    They put up a <strong>whopping 11269 espys</strong> which is a record not likely to ever be beat.
			</p>
			<p>
			    An honorable mention to 2018 SportZone who hit more homeruns than the 2016 team. They were second for most runs scored but dont have as many wins.
			</p>
			<p class="mt-2">
			    However, all of this is in the past.
			    With a new season quickly approaching, there will be more homeruns, more story lines, and, best of all, more beer!
			    Whether you are a 3rd year looking for your first crack at the bat or a fourth year looking to top the rankings.
			    One thing is certain, <strong>History will be made this summer 🥎</strong>!
			</p>
		',
		images.image_id,
		'2024-05-03'
FROM images;

WITH images AS (
	INSERT INTO image (url) VALUES ('https://image-store.fly.storage.tigris.dev/posts/brennan.jpg')
	RETURNING id as image_id
)
INSERT INTO blog_post (author_id, title, summary, html, image_id, date)
SELECT
		(SELECT id FROM player WHERE email ilike 'dallas.fraser.waterloo@gmail.com') AS AuthorId,
		'Champions',
		'Another beautiful hot sunny 🌞 day for the MLSB Alumni Tournament🍻. Ten teams showed up and there were too many home runs to count. However, one team was able to go undefeated on the day and hit in 82 runs⚾...',
		'
		<p>
		    Another beautiful hot sunny 🌞 day for the MLSB Alumni Tournament🍻.
		    Ten teams showed up and there were too many home runs to count.
		    However, one team was able to go undefeated on the day and hit in 82 runs⚾.
		</p>
		<center>
    		<img src="https://image-store.fly.storage.tigris.dev/posts/2024-alumni-champions.jpg"  alt="MLSB Alumni Champion" class="postImage">
		</center>
		<p>
		    <a href="https://mlsb.ca/website/teams/2024/455">Super Seniors</a> beat <a href="https://mlsb.ca/website/teams/2024/395">Jorts</a> in the finals in quite a competitive game.
		    Super Seniors (formerly 2023 convenors) has now won back to back championships.
		    The last team to win back to back championships was back in 2015 when the legendary "Those Guys" won their fourth straight tournament.
		    Time will tell if Super Seniors can go on a run.
		    However, there are some Super Fans out there that aren''t talking 3-peat peat but a minimum 8peat!
		</p>
		<br>
		<br>
		<center>
		    <iframe
		        class="mobile-video"
		        width="560"
		        height="315"
		        src="https://www.youtube.com/embed/NkLjN0UcaTg"
		        frameborder="0"
		        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
		        allowfullscreen
		        title="Minimum 8-peat">
		    </iframe>
		</center>
		
		<br>
		<br>
		<p>
		    One player really stood out in the tournament - hitting 11 homeruns💣.
		    <a href="https://mlsb.ca/website/player/2024/5596">Brennan Lupyrypa</a> now sits only 3 back from <a href="https://mlsb.ca/website/player/2024/355">Jack Romano</a> for all-time homerun leader.
		    With the final week of season coming up, all eyes 👀 will be on Brennan to see if he can go down in MLSB history 📜!
		</p>
		',
		images.image_id,
		'2024-07-20'
FROM images;