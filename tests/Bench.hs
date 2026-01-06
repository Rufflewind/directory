import System.OsPath
import System.Directory.OsPath (getModificationTime)
import Control.Monad

main :: IO ()
main = do
  let rel_path = unsafeEncodeUtf "tests/Main.hs"
  -- print =<< getModificationTime rel_path
  replicateM_ 10000 (getModificationTime rel_path)
