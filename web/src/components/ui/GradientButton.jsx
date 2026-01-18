import React from "react";
import { colors, radius } from "../theme";

const GradientButton = ({
    onClick,
    children,
    style = {},
    type = "button"
}) => {
    return (
        <button
            type={type}
            onClick={onClick}
            style={{
                width: "100%",
                padding: "12px 24px",
                borderRadius: radius.pill,
                border: "none",
                cursor: "pointer",
                fontWeight: "bold",
                color: "#fff",
                background: colors.primaryGradient,
                fontSize: 15,
                ...style,
            }}
        >
            {children}
        </button>
    );
};

export default GradientButton;
