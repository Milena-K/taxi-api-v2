

type InputProps = {
    placeholder: string
    type: string
}



export function Input(props: InputProps) {
    return (
        <>
            <input className="text-center border rounded-lg
                               p-1 border-neutral-400
                                hover:border-gray-50"
                type={props.type}
                placeholder={props.placeholder} />
        </>
    )
}
