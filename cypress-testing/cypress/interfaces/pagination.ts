/** An interface for pagination response. */
export interface Pagination {
    has_next: boolean;
    has_prev: boolean;
    items: Array<any>;
    next_url: string;
    prev_url: string;
    total: number;
    pages: number;
}