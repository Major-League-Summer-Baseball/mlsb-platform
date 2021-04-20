/** The team interface. */
export interface Team {
    team_id: number;
    sponsor_id: number;
    league_id: number;
    color: string;
    year: number;
    espys: number | null;
    team_name: string | null;
};