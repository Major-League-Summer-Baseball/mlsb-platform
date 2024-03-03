/**
 * Submit a score for some given game as a captain of the team.
 * @param {*} captain_information the captain informaiton
 * @param {*} game the game to submit for
 * @param {*} submission_url the URL for submitting the scores to
 * @param {*} next_step_url the next url after game submission
 */
function startApp(captain_information, game, submission_url, next_step_url) {
  const playerStatComponent = Vue.component('player-stat', {
      props: {
          player: Object,
          stat: String,
          number: Number
      },
      template: `
          <div class="form-inline">
              <label>[[player.player_name]]</label>
              <div class="input-group ml-5">
                  <span class="input-group-btn ">
                      <button
                       type="button"
                       class="btn btn-default btn-number"
                       data-type="minus"
                       v-on:click="changeNumber(-1)"
                       :disabled="number <= 0"
                       v-bind:id="'minus-'  + stat + '-' + player.player_id">
                          <span class="glyphicon glyphicon-minus"></span>
                      </button>
                  </span>
                  <input
                   type="text"
                   type="number"
                   min=0
                   v-model="number"
                   class="form-control input-number"
                   v-bind:id="'input-'  + stat + '-' + player.player_id"
                   readonly>
                  <span class="input-group-btn">
                      <button
                       type="button"
                       class="btn btn-default btn-number"
                       data-type="plus"
                       v-on:click="changeNumber(1)"
                       v-bind:id="'plus-'  + stat + '-' + player.player_id">
                          <span class="glyphicon glyphicon-plus"></span>
                      </button>
                  </span>
              </div>
          </div>
      `,
      delimiters: ['[[', ']]'],
      methods: {
          changeNumber: function(direction) {
              if(!this.number) {
                this.number = 0;
              }
              if ((this.number + direction) >= 0) {
                  this.number += direction;
                  if (this.stat == 'ss') {
                      this.player.ss += direction;
                  } else if (this.stat == 'hr') {
                      this.player.hr += direction;
                  }
                  this.$emit('update:number', this.number);
                  this.$emit('update:player', this.player);
              }

              this.$emit('clicked', direction, this.stat);
          }
      }
  });
  const app = new Vue({
      el: '#submitScoreApp',
      data: {
          game_selected: game,
          players: captain_information.players,
          captain_id: captain_information.captain_id,
          team_id: captain_information.team_id,
          hr: 0,
          ss: 0,
          score: 0,
          submitting: false,
      },
      delimiters: ['[[', ']]'],
      methods: {
          gameWasSelected: function(game) {
              this.game_selected = game;
              this.hr = 0;
              this.ss = 0;
              this.score = 0;
              this.players = this.players.map(function(player) {
                  player.hr = 0;
                  player.ss = 0;
                  return player;
              });
          },
          statChange: function(change, stat) {
              if (stat == 'hr') {
                  this.hr += change;
              } else if (stat == 'ss') {
                  this.ss += change;
              }
          },
          submitScore: function() {
              this.submitting = true;
              let hr = [];
              let ss = [];
              this.players.forEach(player => {
                  hr = hr.concat(Array(player.hr).fill(player.player_id));
                  ss = ss.concat(Array(player.ss).fill(player.player_id));
              });
              const scoreData = {
                  'game_id': this.game_selected.game_id,
                  'player_id': this.captain_id,
                  'team_id': this.team_id,
                  'score': this.score,
                  'hr': hr,
                  'ss': ss
              };
              const self = this;
              $.ajax({
                  type: "POST",
                  data: JSON.stringify(scoreData),
                  url: submission_url,
                  contentType: "application/json",
                  dataType: "json",
                  async: true,
                  success: function(success) {
                    self.submitting = false;
                    if (success) {
                        window.location.href = next_step_url;
                    } else {
                        alert("Un-able to submit score");
                    }
                  }, error: function(request, error) {
                    alert("Un-able to submit score");
                    self.game_selected = null;
                    self.submitting = false;
                    console.error(request);
                    console.error(error);
                  }
              });
          }

      }
  });
  if (window.Cypress) {
      window.scoreApp = app;
  }
}

window.startScoreApp = startApp;

