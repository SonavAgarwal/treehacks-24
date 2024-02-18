export interface CodeSnippet {
	code: string;
	path: string;
	url: string;
}

export interface RubricItem {
	name: string;
	criterion: string;
	weight: number;
	score: number;
	codeSnippets: CodeSnippet[];
}

export interface QueryResponse {
	query: string;
	score: number;
	details: RubricItem[];
}
