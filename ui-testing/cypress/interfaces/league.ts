/** The league interface. */
export interface League {
    league_id: number;
    league_name: string;
};

/** A request to join the league or a team. */
export interface JoinLeagueRequest {
    email: string;
    id: number | null;
    pending: boolean;
    player_name: string;
    gender: "m" | "f";
};
