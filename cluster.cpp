#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <unordered_map>
#include <cmath>
#include <map>
#include <limits>


std::map<int, std::vector<int> > pixels;
//std::unordered_map<int, std::vector<int> > pixels;

// Function to read a file
std::vector<std::vector<double> > readFile(const std::string& filename, char delimiter = ' ') {
    std::vector<std::vector<double> > data;

    // Open the file
    std::ifstream file(filename);

    if (!file.is_open()) {
        std::cerr << "Error opening file: " << filename << std::endl;
        return data;
    }

    std::string line;

    // Read each line from the file
    while (std::getline(file, line)) {
        std::vector<double> row;
        std::stringstream ss(line);
        std::string cell;

        // Split the line into cells using the specified delimiter
        while (std::getline(ss, cell, delimiter)) {
            // Convert each cell to a double and add it to the row
            row.push_back(std::stod(cell));
        }

        // Add the row to the data
        data.push_back(row);
    }

    // Close the file
    file.close();

    return data;
}


// Function to evaluate distance

bool IsCloseToAny(int cellID, const std::vector<int>& cluster){
    const std::vector<int> pos1 = pixels[cellID];

    for (int cellIDInCluster : cluster) {

        if (cellID == cellIDInCluster) {
            continue;
        }

        const std::vector<int> pos2 = pixels[cellIDInCluster];
        
        double dist = std::sqrt(std::pow(pos1[0] - pos2[0], 2) +
                                std::pow(pos1[1] - pos2[1], 2) +
                                std::pow(pos1[2] - pos2[2], 2));

        if (dist == 1) {  
            return true;
        }
    }
    return false;
}


// Function to write a file
void writeFile(const std::string& filename, std::unordered_map<int, std::vector<int> > clusters, std::map<int, std::vector<int> > cells) {
//void writeFile(const std::string& filename, std::unordered_map<int, std::vector<int> > clusters, std::unordered_map<int, std::vector<int> > cells) {
    
    
    // Create the file
    std::ofstream outFile(filename);

    
    // Write to file
    int cellID = 0;
    for (const auto& key : clusters) {

        size_t c_size = key.second.size();
        if (c_size < fMINCLUSTSIZE) {
            continue;
        }

        for (const auto& cell : key.second) { 
            //outFile << key.first ; // cellID
            outFile << cellID;
            outFile << "\tfCELLNAME" ; 

            int x_pix = cells.at(cell)[0];
            int y_pix = cells.at(cell)[1];
            int z_pix = cells.at(cell)[2];
            outFile << "\t" << x_pix << "\t" << x_pix << "\t" << y_pix << "\t" << y_pix << "\t" << z_pix << "\t" << z_pix ; // positions
        outFile << "\n";
        }

        cellID++;
    } 

    outFile.close();
    
}


int main() {

    int maxCluster = fMAXCLUSTERSIZE;

    std::vector<std::vector<double> > data = readFile("fFILENAME"); // data is a matrix with the pif file

    // this is the sparse matrix - each key is the cellID and contains x,y,z
    std::vector<int> pixelsUnassigned;
    
    for (const auto& row : data) {
        pixels[row[0]].push_back(row[2]); // pixels is a map whose keys are the cellID and contain a vector with x,y,z
        pixels[row[0]].push_back(row[4]);
        pixels[row[0]].push_back(row[6]);

        pixelsUnassigned.push_back(row[0]);

    }
    

    int initial_cells = pixelsUnassigned.size();
    std::cout << initial_cells << " initial cells" << std::endl;


    int cluster_id = 0;
    std::vector<int>::iterator it;
    std::vector<int> assigned;
    std::unordered_map<int, std::vector<int> > new_cells; // new cells is a map whose keys are the new cellID (clustered) and contains a vector with the original cellIDs


    // for each cell
    for (const auto &cell1 : pixels) {
//    for (size_t i = 0; i < pixelsUnassigned.size(); ++i){

        int cellID1 = cell1.first;
//        int cellID1 = pixelsUnassigned[i];
        
        // has it been assigned to a cluster?    
        if (std::find(assigned.begin(), assigned.end(), cellID1) != assigned.end()) {
            // if yes, skip
            continue;
        }

        //std::cout << "--- Cell 1: " << cellID1 << std::endl;

        //if not, create a new cluster
        new_cells[cluster_id].push_back(cellID1);
        assigned.push_back(cellID1);
        it = find(pixelsUnassigned.begin(),pixelsUnassigned.end(), cellID1);
        pixelsUnassigned.erase(it);


        // in a specifc cluster, for each non-assigned cell
//        for (const auto &cell2 : pixels) {
        int i = 0;
        while (i < pixelsUnassigned.size()){

            if (i == pixelsUnassigned.size()){
                break;
            }

//            int cellID2 = cell2.first;
            int cellID2 = pixelsUnassigned[i];

            //std::cout << "-- Cell 2: " << cellID2 << std::endl;

            // has it been assigned to a cluster?
            if (std::find(assigned.begin(), assigned.end(), cellID2) != assigned.end()) {
                // if yes, skip
                ++i;
                continue;
            }

            

            // is this cell close to any other cell in the cluster?
            bool inTheCluster = IsCloseToAny(cellID2, new_cells[cluster_id]);

            if (inTheCluster) {
                // if yes, add to the cluster list
                new_cells[cluster_id].push_back(cellID2);
                assigned.push_back(cellID2);
                it = find(pixelsUnassigned.begin(),pixelsUnassigned.end(), cellID2);
                pixelsUnassigned.erase(it); 
                i = 0;
            }
            else {
                ++i;
            }

            if (new_cells[cluster_id].size() == maxCluster) {
                break;
            }
        }

        if (new_cells[cluster_id].size() >= fMINCLUSTSIZE) {
            std::cout << "Cluster " << cluster_id << " with " << new_cells[cluster_id].size() << " cells" << std::endl;
            std::cout << assigned.size() << " of " << initial_cells << " assigned, "
                      << (static_cast<double>(assigned.size()) / initial_cells) * 100 << "%" << std::endl;
        }
        ++cluster_id;

    }

    

    std::string outFileName = "fOUTFILENAME";
    writeFile(outFileName,new_cells,pixels);
    

    return 0;
}