import { QueryResponse } from "../types/types";
import { Strength } from "./Strength";

interface Props {
	queryResponse: QueryResponse;
}

const QueryResponseCard = (props: Props) => {
	return (
		<div
			className="strengths-container glasscard"
			style={{
				display: "flex",
				flexDirection: "column",
				gap: "1rem",
			}}
		>
			<div className="heading-subheading">
				<h1>{props.queryResponse.query}</h1>
				{/* <p>{props.queryResponse.query}</p> */}
			</div>
			<div
				style={{
					display: "flex",
					flexDirection: "column",
					gap: "1rem",
					width: "100%",
				}}
			>
				{props.queryResponse.details.map((data, index) => {
					return <Strength key={"strength" + index} rubricItem={data} />;
				})}
			</div>
		</div>
	);
};

export default QueryResponseCard;