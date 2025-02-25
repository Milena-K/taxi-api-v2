
type ButtonProps = {
    text: string,
    onClick: () => void
}

export function Button(props: ButtonProps) {
    return (
        <>
            <button
                className="border rounded rounded-lg
                            px-2 py-1 cursor-pointer
                            border-neutral-400
                            hover:border-gray-50"
                onClick={props.onClick}>
                {props.text}
            </button>
        </>
    )
}
