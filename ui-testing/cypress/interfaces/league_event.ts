/** The game interface. */
export interface LeagueEvent {
    league_event_id: number;
    name: string;
    description: string;
    active: boolean | number;
};
