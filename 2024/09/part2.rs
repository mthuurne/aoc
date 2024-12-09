use std::{env, fs::File, io::{self, BufRead}, path::Path};

fn read_input(path: &Path) -> io::Result<(Vec<(usize, u8)>, Vec<(usize, u8)>)> {
    let file = File::open(path)?;

    let mut files = Vec::new();
    let mut gaps = Vec::new();
    let mut block_idx: usize = 0;
    for line in io::BufReader::new(file).lines() {
        for (seq_idx, ch) in line?.chars().enumerate() {
            let num_blocks = ch.to_digit(10).expect("digit") as u8;
            if (seq_idx & 1) == 0 {
                files.push((block_idx, num_blocks));
            } else {
                gaps.push((block_idx, num_blocks));
            }
            block_idx += num_blocks as usize;
        }
    }

    Ok((files, gaps))
}


fn solve(mut files: Vec<(usize, u8)>, mut gaps: Vec<(usize, u8)>) {
    for file_idx in (0..files.len()).rev() {
        let (from_block, file_size) = files[file_idx];
        for (gap_idx, (to_block, gap_size)) in gaps.iter().enumerate() {
            if *to_block > from_block {
                break
            }
            if *gap_size >= file_size {
                // Update file location.
                files[file_idx] = (*to_block, file_size);
                // Update destination gap.
                gaps[gap_idx] = (to_block + file_size as usize, gap_size - file_size);
                // We don't need to update the source gap, as we'll never use it:
                // files are only moved to the left and we're processing files right-to-left.
                break
            }
        }
    }

    let checksum: usize = files.iter().enumerate().map(|(file_id, (block_id, file_size))| {
        let fs = *file_size as usize;
        (fs * block_id + (fs * (fs - 1) / 2)) * file_id
    }).sum();
    println!("{checksum}");
}

fn main() {
    for arg in env::args().skip(1) {
        println!("=== {arg}");
        let (files, gaps) = read_input(Path::new(&arg)).expect("reading input");
        solve(files, gaps);
    }
}
