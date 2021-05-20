/** The game interface. */
export interface Game {
    game_id: number;
    home_team_id: number;
    home_team: string;
    away_team_id: number;
    away_team: string;
    league_id: number;
    division_id: number;
    date: string;
    time: string;
    status: string;
    field: string;
};
