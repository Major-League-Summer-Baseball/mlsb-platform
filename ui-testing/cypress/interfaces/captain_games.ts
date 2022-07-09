import { Game } from "./game";
import { Player } from "./player";

/** The interface for captain games used by scores and batting apps. */
export interface CaptainGames {
    games: Array<Game>,
    players: Array<Player>
};