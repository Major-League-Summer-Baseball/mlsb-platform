
const GAME_SAVE_ID = 'mlsbGameInformation';
const PREVIOUS_ROSTER_ID = 'mlsbRoster';
const HOMERUN = 'hr';
const TRIPLE = 't';
const DOUBLE = 'd';
const SINGLE = 's';
const SPECIAL_SINGLE = 'ss';
const ERROR = 'e';
const SACRIFICE_FLY = 'sf';
const FIELDER_CHOICE = 'fc';
const LINE_OUT = 'lo';
const GROUND_OUT = 'go';
const FLY_OUT = 'fo';
const STRIKE_OUT = 'k';
const HITS = [SINGLE, SPECIAL_SINGLE, DOUBLE, HOMERUN, TRIPLE];
const SPECIAL_SINGLE_ELIGIBLE = 'f';
const INNING_MAX = 5;

/**
 * Load previous used roster for the batting app
 * @param {*} players a list of players
 * @returns 
 */
function loadPreviousRoster(players) {
    const roster = JSON.parse(localStorage.getItem(PREVIOUS_ROSTER_ID));
    players = JSON.parse(JSON.stringify(players));
    if (roster != null) {
        combined_roster = [];
        roster.forEach(player => {
            const found_player = players.find(p => player.player_id == p.player_id);
            if (found_player) {
                combined_roster.push(found_player);
            }
        });
        // add players for who did not play in the last game
        players.forEach(player => {
            const already_in_lineup = combined_roster.find(p => player.player_id == p.player_id);
            if (!already_in_lineup) {
                combined_roster.push(player);
            }
        });
    } else {
        combined_roster = players;
    }
    return combined_roster;
}

/**
 * Save the previous roster to local storage for potential use later
 * @param {*} roster the roster used
 */
function savePreviousRoster(roster) {
    localStorage.setItem(PREVIOUS_ROSTER_ID, JSON.stringify(roster))
}

/**
 * Save the game to local storage in case they need to reload
 * @param {*} game the game to save
 */
function saveGame(game) {
    localStorage.setItem(GAME_SAVE_ID,  JSON.stringify(game));
}

/**
 * Get the previously save game
 * @returns the saved game otherwise null
 */
function getSavedGame() {
    const game = localStorage.getItem(GAME_SAVE_ID)
    return (game != null) ? JSON.parse(game) : null;
}

/**
 * Get the saved game and remove from local storage
 * @returns remove the previously saved game
 */
function removeSavedGame() {
    return localStorage.removeItem(GAME_SAVE_ID);
}

/**
 * Submit a full box-score for some given game as a captain of the team.
 * @param {*} captain_information the captain informaiton
 * @param {*} game the game to submit for
 * @param {*} submission_url the URL for submitting the scores to
 * @param {*} next_step_url the next url after game submission
 */
function startApp(captain_information, game, submission_url, next_step_url) {
    const previous_game = getSavedGame() || game;
    console.log({previous_game, captain_information});
    const playerEntry = Vue.component('player-row', {
        props: {
            player: Object,
            bats: Array,
            batters: Array
        },
        template: `
            <div v-bind:id="'roster-' + player.player_id" class="player-bats__summary">
                <div v-if="bats.length == 0">
                    <span
                        class="glyphicon glyphicon-circle-arrow-up glyphicon--lg glyphicon--info roster-up"
                        v-if="bats.length == 0"
                        v-bind:id="'rosterUp-' + player.player_id"
                        :disabled="firstBatter()"
                        :class="{'glyphicon--disabled':firstBatter()}"
                        v-on:click="!firstBatter() && $emit('batterup', player)"></span>
                    <span
                        class="glyphicon glyphicon-circle-arrow-down glyphicon--lg glyphicon--info roster-down"
                        v-if="bats.length == 0"
                        v-bind:id="'rosterDown-' + player.player_id"
                        :disabled="lastBatter()"
                        :class="{'glyphicon--disabled':lastBatter()}"
                        v-on:click="!lastBatter() && $emit('batterdown', player)"></span>
                </div>
                <div class="summary__player">
                    [[player.player_name]]
                    <span>(AVG: [[calcualteBattingAverage()]], HR: [[countHomeruns()]] RBI: [[countRbis()]])</span>
                </div>
                <span
                    class="glyphicon glyphicon glyphicon-remove glyphicon--lg glyphicon--danger"
                    v-if="bats.length == 0"
                    v-bind:id="'rosterRemove-' + player.player_id"
                    v-on:click="$emit('removebatter', player)"></span>
            </div>
        `,
        delimiters: ['[[', ']]'],
        methods: {
            calcualteBattingAverage: function() {
                /** Calculate the batting average in the game. */
                bats = this.bats.filter(bat => bat.player_id == this.player.player_id);
                hits = bats.filter(bat => HITS.includes(bat.classification));
                ave = hits.length / bats.length
                return isNaN(ave) ? "---" : ave.toFixed(3);
            },
            countHomeruns: function() {
                /** Count the total number of homeruns. */
                return this.bats.filter(bat => bat.player_id == this.player.player_id && bat.classification == HOMERUN).length;
            },
            countRbis: function() {
                /** Count the number of total runs batted in the game. */
                return this.bats.reduce((partialSum, bat) => partialSum + ((bat.player_id == this.player.player_id) ? bat.rbi: 0), 0);
            },
            firstBatter: function() {
                /** Is the batter the first in the lineup */
                return this.batters[0].player_id == this.player.player_id;
            },
            lastBatter: function() {
                /** Is the batter the last in the lineup */
                return this.batters[this.batters.length - 1].player_id == this.player.player_id;
            }
        }
    });
    const app = new Vue({
        el: '#battingScoreApp',
        data: {
            game_selected: previous_game,
            games: captain_information.games,
            players: loadPreviousRoster(captain_information.players),
            captain_id: captain_information.captain_id,
            team_id: captain_information.team_id,
            batter: 0,
            submitting: false,
            open_inning: false,
        },
        delimiters: ['[[', ']]'],
        methods: {
            advanceBaseRunner: function(base) {
                /** Advances the base runner on the given base and runners ahead of them. */
                if (!this.game_selected.game_state.bases[base]) {
                    // prevent double click
                    return;
                }
                if (base == 2) {
                    // made it home
                    Vue.set(this.game_selected.game_state.bases, base, false);
                    this.runScored();
                } else {
                    // check if lead runner
                    if (this.game_selected.game_state.bases[base + 1]) {
                        this.advanceBaseRunner(base + 1);
                    } 
                    Vue.set(this.game_selected.game_state.bases, base, false);
                    Vue.set(this.game_selected.game_state.bases, base + 1, true);
                }
            },
            baseRunnerOut: function(base) {
                /** A base runner got out either on running or field's choice. */
                if (!this.game_selected.game_state.bases[base]) {
                    // prevent double click
                    return;
                }
                this.game_selected.game_states.push(JSON.parse(JSON.stringify(this.game_selected.game_state)));
                this.gotAnOut();
                this.game_selected.game_state.bases[base] = false;
                
            },
            clearBases: function() {
                /** Clear all the bases. */
                this.game_selected.game_state.bases = [false, false, false];
            },
            currentBatter: function(player) {
                /** Whether the given player is the current batter up. */
                return this.game_selected.game_state.batters[this.game_selected.game_state.batter].player_id == player.player_id;
            },
            gameOver: function() {
                /** The game is over. */
                this.submitting = true;
                const self = this;
                $.ajax({
                    type: "POST",
                    data: JSON.stringify(this.game_selected.game_state.bats),
                    url: submission_url,
                    contentType: "application/json",
                    dataType: "json",
                    async: true,
                    success: function(success) {
                        if (success) {
                            savePreviousRoster(self.game_selected.game_state.batters);
                            self.quitGame();
                        } else {
                            alert("Un-able to submit game");    
                        }
                        self.submitting = false;
                    }, error: function(request, error) {
                        alert("Un-able to submit game");
                        self.game_selected = null;
                        self.submitting = false;
                        console.error(request);
                        console.error(error);
                    }
                });
            },
            gameWasSelected: function(game) {
                /** Handle when a game was selected. */
                game = JSON.parse(JSON.stringify(game));
                game.game_state = this.getFreshGame();
                game.game_states = [];
                this.game_selected = game;
                this.submitting = false;
            },
            getBase: function(base) {
                /** Get the status of the given base. */
                return this.game_selected.game_state.bases[base];
            },
            getFreshGame: function() {
                /** Return a new game */
                return JSON.parse(JSON.stringify({
                    bats: [],
                    batter: 0,
                    inning: 1,
                    outs: 0,
                    batters: JSON.parse(JSON.stringify(this.players)),
                    bases: [false, false, false]
                }));
            },
            gotAnOut: function() {
                /** Updates the out and the inning if max outs were reached. */
                this.game_selected.game_state.outs += 1;
                if (this.game_selected.game_state.outs >= 3) {
                    this.nextInning();
                }
            },
            isBatterEligible: function() {
                /** Is the batter eligible for special singles. */
                const batter = this.game_selected.game_state.batters[this.game_selected.game_state.batter];
                return batter.gender == SPECIAL_SINGLE_ELIGIBLE;
            },
            moveBaseRunner: function(base) {
                /** Move the base runner and saves the state. */
                this.game_selected.game_states.push(JSON.parse(JSON.stringify(this.game_selected.game_state)));
                this.advanceBaseRunner(base);
                saveGame(this.game_selected);
            },
            movePlayerSpot: function(player, up) {
                /** Move the player either up or down in roster */
                const current_spot = this.game_selected.game_state.batters.findIndex((p) => p.player_id  == player.player_id);
                if (up) {
                    var batter = this.game_selected.game_state.batters[current_spot];
                    var previous_batter = this.game_selected.game_state.batters[current_spot - 1];
                    Vue.set(this.game_selected.game_state.batters, current_spot, previous_batter);
                    Vue.set(this.game_selected.game_state.batters, current_spot - 1, batter);
                } else {
                    var batter = this.game_selected.game_state.batters[current_spot];
                    var next_batter = this.game_selected.game_state.batters[current_spot + 1];
                    Vue.set(this.game_selected.game_state.batters, current_spot, next_batter);
                    Vue.set(this.game_selected.game_state.batters, current_spot + 1, batter);
                }
            },
            nextBatter: function() {
                /** Move to the next batter. */
                this.game_selected.game_state.batter = (this.game_selected.game_state.batter + 1) % this.game_selected.game_state.batters.length;
            },
            nextInning: function() {
                /** Move to the next inning. */
                this.clearBases();
                this.game_selected.game_state.inning += 1;
                this.game_selected.game_state.outs = 0;
            },
            quitGame: function() {
                removeSavedGame();
                window.location.href = next_step_url;
            },
            removeBatter: function(player) {
                /** Remove the given player from the batting lineup.*/
                Vue.delete(this.game_selected.game_state.batters, this.game_selected.game_state.batters.indexOf(player));
            },
            restartGame: function() {
                /** Restart the game. */
                this.game_selected.states = [];
                this.game_selected.state = this.getFreshGame();
                this.gameWasSelected(this.game_selected);
            },
            runsThisInning: function() {
                const inning = this.game_selected.game_state.inning;
                return this.game_selected.game_state.bats.reduce((total, bat) => {
                    if (bat.inning === inning) {
                        return total + bat.rbi;
                    }
                    return total;
                }, 0);
            },
            runScored: function() {
                /** Record that a run was scored. */
                const bats = this.game_selected.game_state.bats.length;
                if ((this.runsThisInning() < INNING_MAX && !this.open_inning) || this.open_inning) {
                    this.game_selected.game_state.bats[bats - 1].rbi += 1;
                }
            },
            submitBat: function(stat) {
                /** Handle a bat submission. */
                if (this.submitting) {
                    return;
                }
                this.submitting = true;
                this.game_selected.game_states.push(JSON.parse(JSON.stringify(this.game_selected.game_state)));
                this.game_selected.game_state.bats.push({
                    game_id: this.game_selected.game_id,
                    team_id: this.team_id,
                    player_id: this.game_selected.game_state.batters[this.game_selected.game_state.batter].player_id,
                    rbi: 0,
                    classification: stat,
                    inning: this.game_selected.game_state.inning
                });
                this.nextBatter();
                if (stat == HOMERUN) {
                    this.advanceBaseRunner(0);
                    this.advanceBaseRunner(1);
                    this.advanceBaseRunner(2);
                    this.runScored();
                } else if (stat == TRIPLE) {
                    this.advanceBaseRunner(0);
                    this.advanceBaseRunner(1);
                    this.advanceBaseRunner(2);
                    this.game_selected.game_state.bases[2] = true;
                } else if (stat == DOUBLE) {
                    this.advanceBaseRunner(0);
                    this.advanceBaseRunner(1);
                    this.game_selected.game_state.bases[1] = true;
                } else if (stat == SINGLE || stat == ERROR || stat == SPECIAL_SINGLE) {
                    this.advanceBaseRunner(0);
                    this.game_selected.game_state.bases[0] = true;
                } else if (stat == SACRIFICE_FLY) {
                    this.advanceBaseRunner(2);
                    this.gotAnOut();
                } else if (stat == FLY_OUT || stat == GROUND_OUT || stat == STRIKE_OUT) {
                    this.gotAnOut();
                } else if (stat == FIELDER_CHOICE && !this.game_selected.game_state.bases[0]) {
                    // put a runner on first in case they need one
                    this.game_selected.game_state.bases[0] = true;
                }
                if (this.runsThisInning() == INNING_MAX && !this.open_inning) {
                    this.nextInning();
                }
                saveGame(this.game_selected);
                this.submitting = false;
            },
            toggleOpen: function() {
                this.open_inning = !this.open_inning;
            },
            undo: function() {
                /** Undo the the previous action. */
                this.game_selected.game_state = this.game_selected.game_states.pop();
            }
        },
        computed: {
            can_undo(){
                return this.game_selected.game_states.length > 0 && !this.submitting;
            },
            total_score(){
                return this.game_selected.game_state.bats.reduce((partialSum, bat) => partialSum + bat.rbi, 0);
            }
        },
        created() {
            if (!this.game_selected.game_state) {
                this.gameWasSelected(this.game_selected);
            }
         },
    });
    if (window.Cypress) {
        window.scoreApp = app;
    }
}

//
window.startBattingScoreApp = startApp;