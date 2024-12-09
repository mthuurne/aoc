use std::{env, fs::File, io::{self, BufRead}, path::Path};

fn read_input(path: &Path) -> io::Result<Vec<Option<usize>>> {
    let file = File::open(path)?;

    let mut disk = Vec::new();
    for line in io::BufReader::new(file).lines() {
        for (idx, ch) in line?.chars().enumerate() {
            let num_blocks = ch.to_digit(10).expect("digit");
            let file_id = if (idx & 1) == 0 { Some(idx / 2) } else { None };
            for _ in 0..num_blocks {
                disk.push(file_id);
            }
        }
    }

    Ok(disk)
}


fn solve(mut disk: Vec<Option<usize>>) {
    let mut i = 0;
    let mut j = disk.len() - 1;
    while i < j {
        match disk[i] {
            Some(_) => i += 1,
            None => {
                if disk[j].is_some() {
                    disk[i] = disk[j];
                    disk[j] = None;
                    i += 1;
                }
                j -= 1;
            }
        }
    }

    let checksum: usize = disk.iter().enumerate().filter_map(|(block_id, content)|
        match content {
            Some(file_id) => Some(block_id * *file_id),
            None => None,
        }
    ).sum();
    println!("{checksum}");
}

fn main() {
    for arg in env::args().skip(1) {
        println!("=== {arg}");
        let disk = read_input(Path::new(&arg)).expect("reading input");
        solve(disk);
    }
}
