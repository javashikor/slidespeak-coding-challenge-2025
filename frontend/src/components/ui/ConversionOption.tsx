// Conversion Option Component

interface ConversionOptionProps {
  title: string;
  description: string;
  selected?: boolean;
  onClick?: () => void;
}

export const ConversionOption = ({
  title,
  description,
  selected = false,
  onClick,
}: ConversionOptionProps) => {
  return (
    <div
      className={`bg-white rounded-xl border-2 p-4 cursor-pointer transition-colors ${
        selected
          ? "border-3 border-blue-300 bg-sky-50"
          : "border-gray-200 hover:border-gray-300"
      }`}
      onClick={onClick}
    >
      <div className="flex items-start space-x-3">
        <div
          className={`w-5 h-5 rounded-full border-2 flex items-center justify-center mt-0.5 ${
            selected ? "border-blue-500 bg-white" : "border-gray-300"
          }`}
        >
          {selected && (
            <div className="w-2 h-2 rounded-full bg-blue-500 "></div>
          )}
        </div>
        <div>
          <h4 className=" text-sm text-blue-800">{title}</h4>
          <p className="text-sm text-blue-800">{description}</p>
        </div>
      </div>
    </div>
  );
};
