import { ConversionDone } from "@/components/ConversionDone";
import { ConversionInProgress } from "@/components/ConversionInProgress";
import { FileDragged } from "@/components/FileDragged";
import { PowerPointToPdfConverter } from "@/components/PowerPointToPdfConverter";

const Home = async () => (
  <main className="w-full h-screen flex items-center justify-center">
    <div className="w-full max-w-[420px]">
      <PowerPointToPdfConverter />
      <ConversionInProgress />
      <ConversionDone />
      <FileDragged />
    </div>
  </main>
);

export default Home;
